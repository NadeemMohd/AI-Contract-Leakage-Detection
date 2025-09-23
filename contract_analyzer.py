import re
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from collections import defaultdict
import networkx as nx
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
import pickle
import os
import PyPDF2

class AdvancedContractAnalyzer:
    def __init__(self):
        self.contracts = {}
        self.knowledge_graph = nx.Graph()
        self.vectorizer = TfidfVectorizer(max_features=2000, stop_words='english', ngram_range=(1, 3))
        self.classifier = RandomForestClassifier(n_estimators=200, random_state=42)
        self.clustering_model = KMeans(n_clusters=5, random_state=42)
        self.trained = False
        self.contract_embeddings = {}
        
        # Enhanced patterns for contract term extraction
        self.term_patterns = {
            'pricing': {
                'patterns': [
                    r'\$[\d,]+(?:\.\d{2})?(?:\s*(?:per|/)\s*(?:month|year|user|license|instance))?',
                    r'(?:price|cost|fee|rate|charge)(?:s)?\s*(?:of|is|are|:)\s*\$?[\d,]+(?:\.\d{2})?',
                    r'(?:monthly|annual|yearly)\s*(?:fee|cost|price)\s*(?:of|is|:)?\s*\$?[\d,]+',
                    r'(?:subscription|license)\s*(?:fee|cost)\s*(?:of|is|:)?\s*\$?[\d,]+'
                ],
                'weight': 1.0
            },
            'penalties': {
                'patterns': [
                    r'penalty(?:ies)?\s*(?:of|is|are|:)\s*\$?[\d,]+(?:\.\d{2})?',
                    r'(?:breach|violation|default)\s*(?:penalty|fine|fee)',
                    r'(?:late|overdue)\s*(?:payment|fee|penalty)',
                    r'(?:termination|cancellation)\s*(?:fee|penalty|charge)'
                ],
                'weight': 1.5
            },
            'renewals': {
                'patterns': [
                    r'(?:auto|automatic)(?:ally)?\s*(?:renew|renewal)',
                    r'(?:renewal|renew)\s*(?:period|term|date)',
                    r'(?:expire|expiration)\s*(?:date|on)',
                    r'(?:term|contract)\s*(?:expires|ends)\s*(?:on|at)'
                ],
                'weight': 1.2
            },
            'volume_discounts': {
                'patterns': [
                    r'volume\s*(?:discount|pricing|tier)',
                    r'(?:bulk|quantity)\s*(?:discount|pricing)',
                    r'(?:tier|tiered)\s*(?:pricing|discount)',
                    r'(?:discount|reduced\s*price)\s*(?:for|when)\s*(?:volume|bulk|quantity)'
                ],
                'weight': 1.3
            },
            'hardware_specs': {
                'patterns': [
                    r'(?:cpu|processor)\s*(?:cores?|units?)?\s*:?\s*[\d]+',
                    r'(?:memory|ram)\s*:?\s*[\d]+\s*(?:gb|mb|tb)',
                    r'(?:storage|disk)\s*:?\s*[\d]+\s*(?:gb|mb|tb)',
                    r'(?:server|instance|vm)\s*(?:type|size|configuration)',
                    r'(?:compute|processing)\s*(?:power|capacity|units?)'
                ],
                'weight': 1.1
            },
            'sla_terms': {
                'patterns': [
                    r'(?:sla|service\s*level\s*agreement)',
                    r'uptime\s*(?:guarantee|requirement)\s*(?:of)?\s*[\d.]+%',
                    r'availability\s*(?:guarantee|requirement)\s*(?:of)?\s*[\d.]+%',
                    r'response\s*time\s*(?:of|within)?\s*[\d]+\s*(?:hours?|minutes?|days?)',
                    r'(?:performance|reliability)\s*(?:guarantee|standard|requirement)'
                ],
                'weight': 1.4
            },
            'license_terms': {
                'patterns': [
                    r'(?:user|seat|named)\s*license',
                    r'concurrent\s*(?:user|license)',
                    r'(?:per|/)\s*(?:user|seat|license)',
                    r'license\s*(?:type|model|agreement)',
                    r'(?:usage|utilization)\s*(?:limit|restriction|cap)'
                ],
                'weight': 1.2
            }
        }
    
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
        """Enhanced contract term extraction with weighted scoring"""
        terms = {}
        text_lower = text.lower()
        
        for category, config in self.term_patterns.items():
            matches = []
            scores = []
            
            for pattern in config['patterns']:
                pattern_matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in pattern_matches:
                    match_text = match.group()
                    # Calculate relevance score based on context
                    context_start = max(0, match.start() - 50)
                    context_end = min(len(text), match.end() + 50)
                    context = text[context_start:context_end].lower()
                    
                    # Score based on surrounding keywords
                    relevance_score = config['weight']
                    if any(keyword in context for keyword in ['contract', 'agreement', 'terms']):
                        relevance_score *= 1.2
                    
                    matches.append(match_text)
                    scores.append(relevance_score)
            
            # Sort by relevance and take top matches
            if matches:
                sorted_matches = sorted(zip(matches, scores), key=lambda x: x[1], reverse=True)
                terms[category] = {
                    'matches': [match for match, _ in sorted_matches[:10]],
                    'scores': [score for _, score in sorted_matches[:10]],
                    'total_score': sum(score for _, score in sorted_matches)
                }
            else:
                terms[category] = {'matches': [], 'scores': [], 'total_score': 0}
        
        return terms
    
    def detect_advanced_leakage(self, contract_type):
        """Advanced leakage detection with risk scoring"""
        leakage_issues = []
        
        for contract_id, contract_data in self.contracts.items():
            if contract_type in contract_id:
                terms = contract_data['terms']
                risk_score = 0
                
                # Hardware usage vs commitment analysis
                hardware_score = terms.get('hardware_specs', {}).get('total_score', 0)
                pricing_score = terms.get('pricing', {}).get('total_score', 0)
                
                if hardware_score > 0 and pricing_score > 0:
                    # Check for potential over-provisioning
                    if hardware_score > pricing_score * 1.5:
                        risk_score += 30
                        leakage_issues.append({
                            'contract': contract_id,
                            'type': 'Hardware Over-Provisioning',
                            'description': 'High hardware specifications relative to pricing terms suggest potential over-provisioning',
                            'severity': 'High',
                            'risk_score': 30,
                            'estimated_impact': '$75,000'
                        })
                
                # Renewal penalty analysis
                renewal_score = terms.get('renewals', {}).get('total_score', 0)
                penalty_score = terms.get('penalties', {}).get('total_score', 0)
                
                if renewal_score > 0 and penalty_score == 0:
                    risk_score += 25
                    leakage_issues.append({
                        'contract': contract_id,
                        'type': 'Missing Renewal Penalties',
                        'description': 'Renewal terms present but no penalty clauses for missed renewals',
                        'severity': 'High',
                        'risk_score': 25,
                        'estimated_impact': '$50,000'
                    })
                
                # Volume discount optimization
                volume_score = terms.get('volume_discounts', {}).get('total_score', 0)
                if volume_score > 0:
                    # Check if volume discounts are being utilized
                    if volume_score < 2.0:  # Low utilization indicator
                        risk_score += 20
                        leakage_issues.append({
                            'contract': contract_id,
                            'type': 'Underutilized Volume Discounts',
                            'description': 'Volume discount opportunities may not be fully utilized',
                            'severity': 'Medium',
                            'risk_score': 20,
                            'estimated_impact': '$35,000'
                        })
                
                # SLA compliance monitoring
                sla_score = terms.get('sla_terms', {}).get('total_score', 0)
                if sla_score > 0 and penalty_score == 0:
                    risk_score += 15
                    leakage_issues.append({
                        'contract': contract_id,
                        'type': 'SLA Without Penalties',
                        'description': 'SLA terms defined but no penalty structure for non-compliance',
                        'severity': 'Medium',
                        'risk_score': 15,
                        'estimated_impact': '$25,000'
                    })
                
                # License optimization
                license_score = terms.get('license_terms', {}).get('total_score', 0)
                if license_score > 0:
                    # Check for potential license waste
                    license_matches = terms.get('license_terms', {}).get('matches', [])
                    if any('concurrent' in match for match in license_matches):
                        risk_score += 10
                        leakage_issues.append({
                            'contract': contract_id,
                            'type': 'License Optimization Opportunity',
                            'description': 'Concurrent licensing model may offer cost savings',
                            'severity': 'Low',
                            'risk_score': 10,
                            'estimated_impact': '$15,000'
                        })
        
        return leakage_issues
    
    def build_enhanced_knowledge_graph(self):
        """Build enhanced knowledge graph with relationship weights"""
        self.knowledge_graph.clear()
        
        # Add company nodes
        companies = ['Azure', 'NadComms', 'CustomerA', 'CustomerB', 'CustomerC']
        for company in companies:
            self.knowledge_graph.add_node(company, type='company')
        
        # Add contract nodes and relationships
        for contract_id, contract_data in self.contracts.items():
            self.knowledge_graph.add_node(contract_id, 
                                        type='contract',
                                        **contract_data['metadata'])
            
            # Determine relationships based on contract type
            if 'azure' in contract_id.lower() and 'nadcomms' in contract_id.lower():
                self.knowledge_graph.add_edge('Azure', 'NadComms', 
                                            relationship='infrastructure_provider',
                                            contract=contract_id,
                                            weight=1.0)
                self.knowledge_graph.add_edge('NadComms', contract_id,
                                            relationship='party_to_contract',
                                            weight=1.0)
                self.knowledge_graph.add_edge('Azure', contract_id,
                                            relationship='party_to_contract',
                                            weight=1.0)
            
            elif 'nadcomms' in contract_id.lower() and 'customer' in contract_id.lower():
                customer = None
                if 'customera' in contract_id.lower():
                    customer = 'CustomerA'
                elif 'customerb' in contract_id.lower():
                    customer = 'CustomerB'
                elif 'customerc' in contract_id.lower():
                    customer = 'CustomerC'
                
                if customer:
                    self.knowledge_graph.add_edge('NadComms', customer,
                                                relationship='service_provider',
                                                contract=contract_id,
                                                weight=1.0)
                    self.knowledge_graph.add_edge('NadComms', contract_id,
                                                relationship='party_to_contract',
                                                weight=1.0)
                    self.knowledge_graph.add_edge(customer, contract_id,
                                                relationship='party_to_contract',
                                                weight=1.0)
    
    def generate_contract_similarity_matrix(self):
        """Generate similarity matrix between contracts"""
        if not self.contracts:
            return None
        
        contract_texts = []
        contract_ids = []
        
        for contract_id, contract_data in self.contracts.items():
            contract_texts.append(contract_data['text'])
            contract_ids.append(contract_id)
        
        # Create TF-IDF vectors
        tfidf_matrix = self.vectorizer.fit_transform(contract_texts)
        
        # Calculate similarity matrix
        similarity_matrix = cosine_similarity(tfidf_matrix)
        
        return pd.DataFrame(similarity_matrix, 
                          index=contract_ids, 
                          columns=contract_ids)
    
    def predict_contract_risk(self, contract_text):
        """Predict risk level for a new contract"""
        if not self.trained:
            return None
        
        # Extract features
        terms = self.extract_contract_terms(contract_text)
        
        # Calculate risk features
        features = []
        for category in self.term_patterns.keys():
            score = terms.get(category, {}).get('total_score', 0)
            features.append(score)
        
        # Normalize features
        features = np.array(features).reshape(1, -1)
        
        # Predict using trained model (simplified for demo)
        risk_probability = np.random.random()  # Placeholder
        
        if risk_probability > 0.7:
            return 'High Risk'
        elif risk_probability > 0.4:
            return 'Medium Risk'
        else:
            return 'Low Risk'
    
    def generate_compliance_report(self):
        """Generate comprehensive compliance and leakage report"""
        report = {
            'summary': {
                'total_contracts': len(self.contracts),
                'high_risk_contracts': 0,
                'medium_risk_contracts': 0,
                'low_risk_contracts': 0,
                'total_estimated_savings': 0
            },
            'contract_analysis': {},
            'recommendations': [],
            'knowledge_graph_metrics': {
                'nodes': self.knowledge_graph.number_of_nodes(),
                'edges': self.knowledge_graph.number_of_edges(),
                'density': nx.density(self.knowledge_graph) if self.knowledge_graph.number_of_nodes() > 0 else 0
            }
        }
        
        # Analyze each contract
        for contract_id, contract_data in self.contracts.items():
            contract_type = 'azure' if 'azure' in contract_id.lower() else 'customer'
            leakage_issues = self.detect_advanced_leakage(contract_type)
            
            # Calculate risk level
            total_risk_score = sum(issue['risk_score'] for issue in leakage_issues)
            if total_risk_score > 50:
                risk_level = 'High'
                report['summary']['high_risk_contracts'] += 1
            elif total_risk_score > 20:
                risk_level = 'Medium'
                report['summary']['medium_risk_contracts'] += 1
            else:
                risk_level = 'Low'
                report['summary']['low_risk_contracts'] += 1
            
            # Calculate estimated savings
            estimated_savings = sum(
                int(issue['estimated_impact'].replace('$', '').replace(',', ''))
                for issue in leakage_issues
            )
            report['summary']['total_estimated_savings'] += estimated_savings
            
            report['contract_analysis'][contract_id] = {
                'risk_level': risk_level,
                'risk_score': total_risk_score,
                'leakage_issues': leakage_issues,
                'estimated_savings': estimated_savings
            }
        
        # Generate recommendations
        if report['summary']['high_risk_contracts'] > 0:
            report['recommendations'].append({
                'priority': 'High',
                'action': 'Immediate review of high-risk contracts required',
                'description': f"{report['summary']['high_risk_contracts']} contracts have high leakage risk"
            })
        
        if report['summary']['total_estimated_savings'] > 100000:
            report['recommendations'].append({
                'priority': 'High',
                'action': 'Implement automated contract monitoring',
                'description': f"Potential savings of ${report['summary']['total_estimated_savings']:,} identified"
            })
        
        return report
    
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
        
        try:
            # Vectorize text
            X = self.vectorizer.fit_transform(texts)
            
            # Train classifier if we have enough data
            if len(texts) >= 2:
                from sklearn.model_selection import train_test_split
                if len(texts) > 2:
                    X_train, X_test, y_train, y_test = train_test_split(X, labels, test_size=0.2, random_state=42)
                else:
                    X_train, y_train = X, labels
                
                self.classifier.fit(X_train, y_train)
                self.trained = True
                
                # Save model
                os.makedirs('models', exist_ok=True)
                with open('models/contract_model.pkl', 'wb') as f:
                    pickle.dump({
                        'vectorizer': self.vectorizer,
                        'classifier': self.classifier
                    }, f)
                
                return True
        except Exception as e:
            print(f"Model training error: {str(e)}")
            return False
        
        return False
