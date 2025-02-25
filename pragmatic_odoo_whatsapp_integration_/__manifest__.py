{
    'name': 'Whatsapp-all-in-one Dashboard',
    'version': '16.0.5',
    'category': 'Connector',
    'author': 'Pragmatic TechSoft Pvt Ltd.',
    'website': 'pragtech.co.in',
    'summary': 'whatsapp connector integration odoo Whatsapp crm Whatsapp lead Whatsapp task Whatsapp sale order Whatsapp purchase order Whatsapp invoice Whatsapp payment reminder Whatsapp pos Whatsapp automation Whatsapp point of sale livechat whatsapp business',
    'description': """
Whatsapp Odoo All In One Integration
====================================
Whatsapp is an immensely popular chatting app used by 1.5 Billion people worldwide.
It has an easy interface and can be used powerfully with Odoo.
Pragmatic has developed an Odoo app which allows users to use the Whatsapp Application to send messages via Odoo.
We can send messages from Contacts, Sales, Accounts invoice, Accounts Payments, Credit Notes, Delivery orders, 
Point of sale, Purchase orders, Project Task, CRM Lead, Payment Reminder, User signup page via the same application. 
Let us have a look at how this works inside Odoo.

Features of Whatsapp Odoo All in one Integration
------------------------------------------------
    * Robust, Reliable and Server based and it can handle large volumes of Messages
    * Permission to enable whatsapp messages on Sales orders, Purchase order, Accounts invoice/payments, Delivery orders
    * Send message Configuration
        I Set Signature:to whatsapp Messages
        II Add to chatter
        III Add order product information in message such as order amount.
        IV Add product details in message such as name and other details:
    * In CRM, when lead or opportunity will be created then a message will be sent to the salesperson.
    * In Project Management when when task is created then a WhatsApp message will be sent to the assigned user.
    * If user sends a reply to task message as done then in odoo project task state is changed to done
    * Send Payment reminder message to customer.
    * Send messages to single or multiple Contacts within Odoo along with multiple attachments in different formats such as doc, pdf, image, audio, video
    * In the Point of sale Odoo app when an order is confirmed, send order details message to customer
    * Send message when a user signs up on the Odoo website page.

On Ubuntu server need to execute following command

``sudo pip3 install phonenumbers``
    """,
    'depends': ['base', 'mail', 'base_setup', 'bus', 'web_tour', 'product', 'purchase', 'sale', 'account', 'contacts'],
    'data': [
    ],
    'images': ['static/description/whatsapp_all_in_one_dashboard.gif'],
    'live_test_url': 'https://www.pragtech.co.in/company/proposal-form.html?id=103&name=odoo-whatsapp-integration',
    'price': 117,
    'currency': 'USD',
    'license': 'OPL-1',
    'application': False,
    'auto_install': False,
    'installable': True,
}
