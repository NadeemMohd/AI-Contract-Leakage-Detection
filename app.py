from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
from datetime import datetime
from werkzeug.utils import secure_filename
import PyPDF2
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import networkx as nx
import pickle
import re
from collections import defaultdict
from contract_analyzer import AdvancedContractAnalyzer

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Ensure upload directories exist
os.makedirs('uploads/azure-nadcomms', exist_ok=True)
os.makedirs('uploads/nadcomms-customerA', exist_ok=True)
os.makedirs('uploads/nadcomms-customerB', exist_ok=True)
os.makedirs('uploads/nadcomms-customerC', exist_ok=True)
os.makedirs('models', exist_ok=True)
os.makedirs('analysis_results', exist_ok=True)

class ContractAnalyzer:
    def __init__(self):
        self.contracts = {}
        self.knowledge_graph = nx.Graph()
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.trained = False
        
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def extract_contract_terms(self, text):
        """Extract key contract terms using NLP"""
        terms = {
            'pricing': [],
            'penalties': [],
            'renewals': [],
            'volume_discounts': [],
            'hardware_specs': [],
            'license_terms': [],
            'sla_terms': []
        }
        
        # Define patterns for different contract terms
        patterns = {
            'pricing': r'(?i)\$[\d,]+(?:\.\d{2})?|price|cost|fee|rate',
            'penalties': r'(?i)penalty|fine|breach|violation|default',
            'renewals': r'(?i)renew|renewal|expire|expiration|term',
            'volume_discounts': r'(?i)volume|discount|tier|bulk|quantity',
            'hardware_specs': r'(?i)cpu|memory|ram|storage|server|instance',
            'license_terms': r'(?i)license|licensing|usage|user|seat',
            'sla_terms': r'(?i)sla|uptime|availability|performance|response'
        }
        
        for category, pattern in patterns.items():
            matches = re.findall(pattern, text, re.IGNORECASE)
            terms[category] = matches[:10]  # Limit to first 10 matches
        
        return terms
    
    def build_knowledge_graph(self):
        """Build knowledge graph from contracts"""
        self.knowledge_graph.clear()
        
        for contract_id, contract_data in self.contracts.items():
            self.knowledge_graph.add_node(contract_id, **contract_data['metadata'])
            
            # Add edges based on relationships
            if 'azure' in contract_id.lower() and 'nadcomms' in contract_id.lower():
                self.knowledge_graph.add_edge('Azure', 'NadComms', relationship='hosting')
            elif 'nadcomms' in contract_id.lower() and 'customer' in contract_id.lower():
                customer = contract_data['metadata'].get('customer', 'Unknown')
                self.knowledge_graph.add_edge('NadComms', customer, relationship='service')
    
    def detect_leakage(self, contract_type):
        """Detect potential revenue leakage"""
        leakage_issues = []
        
        for contract_id, contract_data in self.contracts.items():
            if contract_type in contract_id:
                terms = contract_data['terms']
                
                # Check for hardware usage vs commitment
                if terms['hardware_specs'] and terms['pricing']:
                    leakage_issues.append({
                        'contract': contract_id,
                        'type': 'Hardware Usage Mismatch',
                        'description': 'Potential mismatch between committed and actual hardware usage',
                        'severity': 'Medium'
                    })
                
                # Check for missed renewal opportunities
                if terms['renewals'] and not terms['penalties']:
                    leakage_issues.append({
                        'contract': contract_id,
                        'type': 'Missed Renewal Penalty',
                        'description': 'No penalty clauses found for missed renewals',
                        'severity': 'High'
                    })
                
                # Check for volume discount opportunities
                if terms['volume_discounts'] and terms['pricing']:
                    leakage_issues.append({
                        'contract': contract_id,
                        'type': 'Volume Discount Opportunity',
                        'description': 'Potential unclaimed volume discounts',
                        'severity': 'Medium'
                    })
        
        return leakage_issues
    
    def train_model(self):
        """Train ML model on contract data"""
        if not self.contracts:
            return False
        
        # Prepare training data
        texts = []
        labels = []
        
        for contract_id, contract_data in self.contracts.items():
            texts.append(contract_data['text'])
            # Simple labeling based on contract type
            if 'azure' in contract_id.lower():
                labels.append('infrastructure')
            else:
                labels.append('service')
        
        if len(set(labels)) < 2:
            return False
        
        # Vectorize text
        X = self.vectorizer.fit_transform(texts)
        
        # Train classifier
        X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)
        self.classifier.fit(X_train, y_train)
        self.trained = True
        
        # Save model
        with open('models/contract_model.pkl', 'wb') as f:
            pickle.dump({
                'vectorizer': self.vectorizer,
                'classifier': self.classifier
            }, f)
        
        return True

# Initialize advanced analyzer
analyzer = AdvancedContractAnalyzer()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'})
    
    file = request.files['file']
    contract_type = request.form.get('contract_type')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'})
    
    if file and file.filename.lower().endswith('.pdf'):
        filename = secure_filename(file.filename)
        
        # Determine upload folder based on contract type
        folder_map = {
            'azure-nadcomms': 'uploads/azure-nadcomms',
            'nadcomms-customerA': 'uploads/nadcomms-customerA',
            'nadcomms-customerB': 'uploads/nadcomms-customerB',
            'nadcomms-customerC': 'uploads/nadcomms-customerC'
        }
        
        upload_folder = folder_map.get(contract_type, 'uploads')
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        # Process the contract
        text = analyzer.extract_text_from_pdf(filepath)
        terms = analyzer.extract_contract_terms(text)
        
        # Store contract data
        contract_id = f"{contract_type}_{filename}"
        analyzer.contracts[contract_id] = {
            'text': text,
            'terms': terms,
            'metadata': {
                'filename': filename,
                'contract_type': contract_type,
                'upload_date': datetime.now().isoformat(),
                'customer': contract_type.split('-')[-1] if 'customer' in contract_type else None
            }
        }
        
        return jsonify({'success': True, 'message': f'Contract {filename} uploaded successfully'})
    
    return jsonify({'error': 'Invalid file type. Please upload a PDF file.'})

@app.route('/analyze', methods=['POST'])
def analyze_contracts():
    if not analyzer.contracts:
        return jsonify({'error': 'No contracts uploaded yet'})
    
    # Build enhanced knowledge graph
    analyzer.build_enhanced_knowledge_graph()
    
    # Train model
    training_success = analyzer.train_model()
    
    # Detect advanced leakage for different contract types
    azure_leakage = analyzer.detect_advanced_leakage('azure')
    customer_leakage = analyzer.detect_advanced_leakage('customer')
    
    # Generate comprehensive compliance report
    compliance_report = analyzer.generate_compliance_report()
    
    # Prepare analysis results
    results = {
        'model_trained': training_success,
        'total_contracts': len(analyzer.contracts),
        'knowledge_graph_nodes': analyzer.knowledge_graph.number_of_nodes(),
        'knowledge_graph_edges': analyzer.knowledge_graph.number_of_edges(),
        'azure_leakage_issues': azure_leakage,
        'customer_leakage_issues': customer_leakage,
        'compliance_report': compliance_report,
        'analysis_date': datetime.now().isoformat()
    }
    
    # Save results
    with open('analysis_results/latest_analysis.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    return jsonify(results)

@app.route('/results')
def view_results():
    try:
        with open('analysis_results/latest_analysis.json', 'r') as f:
            results = json.load(f)
        return render_template('results.html', results=results)
    except FileNotFoundError:
        return render_template('results.html', results=None)

@app.route('/contracts')
def list_contracts():
    contract_list = []
    for contract_id, contract_data in analyzer.contracts.items():
        contract_list.append({
            'id': contract_id,
            'filename': contract_data['metadata']['filename'],
            'type': contract_data['metadata']['contract_type'],
            'upload_date': contract_data['metadata']['upload_date']
        })
    return jsonify(contract_list)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
