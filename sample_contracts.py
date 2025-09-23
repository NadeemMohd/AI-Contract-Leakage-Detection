import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime, timedelta

def create_sample_contracts():
    """Create sample PDF contracts for testing the system"""
    
    # Create sample contracts directory
    os.makedirs('sample_contracts', exist_ok=True)
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    # Azure-NadComms Contract
    azure_contract = create_azure_nadcomms_contract()
    save_contract_pdf(azure_contract, 'sample_contracts/Azure_NadComms_Infrastructure_Agreement.pdf', title_style, styles)
    
    # Customer A Contract
    customer_a_contract = create_customer_contract('CustomerA', 'Enterprise ERP Solution')
    save_contract_pdf(customer_a_contract, 'sample_contracts/NadComms_CustomerA_Service_Agreement.pdf', title_style, styles)
    
    # Customer B Contract
    customer_b_contract = create_customer_contract('CustomerB', 'Advanced Analytics Platform')
    save_contract_pdf(customer_b_contract, 'sample_contracts/NadComms_CustomerB_Service_Agreement.pdf', title_style, styles)
    
    # Customer C Contract
    customer_c_contract = create_customer_contract('CustomerC', 'Cloud Integration Suite')
    save_contract_pdf(customer_c_contract, 'sample_contracts/NadComms_CustomerC_Service_Agreement.pdf', title_style, styles)
    
    print("Sample contracts created successfully!")

def create_azure_nadcomms_contract():
    """Create Azure-NadComms infrastructure contract content"""
    contract_date = datetime.now().strftime("%B %d, %Y")
    expiry_date = (datetime.now() + timedelta(days=365)).strftime("%B %d, %Y")
    
    return f"""
CLOUD INFRASTRUCTURE SERVICE AGREEMENT

This Cloud Infrastructure Service Agreement ("Agreement") is entered into on {contract_date}, between Microsoft Azure ("Azure") and NadComms Technologies Ltd. ("NadComms").

1. SERVICE SPECIFICATIONS
Azure shall provide cloud infrastructure services including:
- Compute instances: 50 Standard D4s v3 (4 vCPU, 16 GB RAM each)
- Storage: 10 TB Premium SSD storage
- Network: 1 Gbps dedicated bandwidth
- Operating System: Windows Server 2022 licenses for all instances
- Database: Azure SQL Database Premium tier

2. PRICING TERMS
Monthly service fee: $45,000 per month
Annual commitment discount: 15% reduction for 12-month prepayment
Volume discount: Additional 5% discount for usage above 80% of committed resources
Payment terms: Net 30 days from invoice date

3. SERVICE LEVEL AGREEMENT (SLA)
Uptime guarantee: 99.9% monthly uptime
Response time: Critical issues within 2 hours, standard issues within 8 hours
Performance guarantee: CPU utilization monitoring with alerts at 85% threshold
Availability monitoring: 24/7 automated monitoring with instant notifications

4. RENEWAL AND TERMINATION
Contract term: 12 months from effective date
Automatic renewal: Contract automatically renews for additional 12-month periods
Termination notice: 90 days written notice required for non-renewal
Early termination penalty: 25% of remaining contract value

5. PENALTIES AND COMPLIANCE
SLA breach penalty: 5% monthly fee credit for each 0.1% below 99.9% uptime
Late payment penalty: 2% per month on overdue amounts
Resource over-usage: 150% of standard rate for usage exceeding committed resources
Security compliance: SOC 2 Type II certification required

6. VOLUME COMMITMENTS
Minimum monthly usage: 70% of committed resources
Volume tier 1: 70-85% usage - standard pricing
Volume tier 2: 85-95% usage - 3% discount
Volume tier 3: 95%+ usage - 5% additional discount

Contract expires on: {expiry_date}
Renewal deadline: 90 days prior to expiration

Azure Representative: John Smith, Enterprise Sales Manager
NadComms Representative: Sarah Johnson, CTO

This agreement constitutes the entire understanding between the parties regarding cloud infrastructure services.
"""

def create_customer_contract(customer_name, service_name):
    """Create customer service contract content"""
    contract_date = datetime.now().strftime("%B %d, %Y")
    expiry_date = (datetime.now() + timedelta(days=730)).strftime("%B %d, %Y")  # 2 years
    
    pricing_map = {
        'CustomerA': {'base': 25000, 'users': 500, 'discount': 10},
        'CustomerB': {'base': 18000, 'users': 300, 'discount': 8},
        'CustomerC': {'base': 32000, 'users': 750, 'discount': 12}
    }
    
    pricing = pricing_map.get(customer_name, {'base': 20000, 'users': 400, 'discount': 10})
    
    return f"""
SOFTWARE AS A SERVICE AGREEMENT

This Software as a Service Agreement ("Agreement") is entered into on {contract_date}, between NadComms Technologies Ltd. ("NadComms") and {customer_name} Corporation ("{customer_name}").

1. SERVICE DESCRIPTION
NadComms shall provide {service_name} including:
- Cloud-based enterprise software platform
- User licenses for up to {pricing['users']} named users
- 24/7 technical support and maintenance
- Data backup and disaster recovery services
- Regular software updates and security patches

2. PRICING AND PAYMENT TERMS
Monthly subscription fee: ${pricing['base']:,} per month
Per-user licensing: $50 per additional user above {pricing['users']} users
Annual prepayment discount: {pricing['discount']}% discount for full year payment
Volume discount: Additional 5% discount for user count above {int(pricing['users'] * 1.2)} users
Payment terms: Monthly in advance, Net 15 days

3. SERVICE LEVEL AGREEMENT
System availability: 99.5% monthly uptime guarantee
Response time: Priority 1 issues within 4 hours, Priority 2 within 24 hours
Performance standard: Page load times under 3 seconds for 95% of requests
Data backup: Daily automated backups with 30-day retention

4. USER LICENSE TERMS
Named user licenses: Each license assigned to specific individual
Concurrent usage: Maximum 85% of licensed users online simultaneously
License transfer: Users can be reassigned with 48-hour notice
Usage monitoring: Monthly reports on user activity and system utilization

5. RENEWAL AND TERMINATION
Contract term: 24 months from effective date
Automatic renewal: Renews for 12-month periods unless terminated
Termination notice: 60 days written notice required
Data retention: 90 days after termination for data export

6. PENALTIES AND BREACH TERMS
SLA breach credit: 2% monthly fee credit for each hour below 99.5% uptime
Late payment penalty: 1.5% per month on overdue amounts
Breach of user limits: $100 per unauthorized user per month
Early termination fee: 50% of remaining contract value

7. VOLUME PRICING TIERS
Tier 1 (up to {pricing['users']} users): Standard pricing
Tier 2 ({pricing['users']+1}-{int(pricing['users']*1.5)} users): 5% discount on additional users
Tier 3 ({int(pricing['users']*1.5)+1}+ users): 10% discount on additional users

8. PERFORMANCE COMMITMENTS
System response time: Average 2 seconds for standard operations
Data processing: Batch jobs completed within 4-hour windows
Report generation: Standard reports within 30 seconds
Custom integrations: API response time under 500ms

Contract expires on: {expiry_date}
Renewal review date: 90 days prior to expiration

NadComms Representative: Michael Chen, VP of Sales
{customer_name} Representative: [To be filled]

This agreement represents the complete terms for software services between the parties.
"""

def save_contract_pdf(content, filename, title_style, styles):
    """Save contract content as PDF file"""
    try:
        doc = SimpleDocTemplate(filename, pagesize=letter,
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=18)
        
        story = []
        
        # Split content into paragraphs
        paragraphs = content.strip().split('\n\n')
        
        for i, para in enumerate(paragraphs):
            if i == 0:  # Title
                story.append(Paragraph(para, title_style))
            else:
                story.append(Paragraph(para, styles['Normal']))
            story.append(Spacer(1, 12))
        
        doc.build(story)
        print(f"Created: {filename}")
        
    except Exception as e:
        print(f"Error creating {filename}: {str(e)}")

if __name__ == "__main__":
    create_sample_contracts()
