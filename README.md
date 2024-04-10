# Prompt Base

Prompt Base is a Streamlit-based application that allows users to create, store, search, and manage ChatGPT prompts. With features such as marking prompts as favorites and the ability to search through saved prompts, Prompt Base is an excellent tool for anyone looking to streamline their ChatGPT prompt management process.

## How to Run

To run the Prompt Base app on your local machine, follow these steps:

```
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

streamlit run app.py
```

## How to Use

After launching the app, you'll be greeted with a simple and intuitive UI:

- Creating a Prompt: Enter a title and the prompt content in the designated text fields, and mark it as a favorite if desired. Submit by clicking the "Create Prompt" button.
- Viewing and Searching Prompts: Use the search bar to filter prompts by title or view all by leaving it empty. You can also filter prompts based on their favorite status.
- Editing and Deleting Prompts: Each saved prompt can be edited or deleted directly from its expanded view.

### Using Azure PostgreSQL as Database

This application is configured to use Azure PostgreSQL as its database backend. Follow these steps to set up your Azure PostgreSQL database and connect it to the app.

- Setting Up Azure PostgreSQL
- Create an Azure PostgreSQL Database Instance: Log in to the Azure Portal.
- Navigate to "Databases" and select "Azure Database for PostgreSQL".
- Click on "Add" to create a new database instance. Follow the prompts to configure your database, such as selecting the database version, compute and storage options, and setting up the administrator account details.
- Configure Firewall Rules:
    - Once your database instance is set up, navigate to its overview page.
    - Under "Settings", find and select "Connection security".
    - Add a new rule to allow connections from your IP address. Azure might also provide an option to allow connections from Azure services or add a range of trusted IP addresses.

### Configuring the Application to Use Azure PostgreSQL

1. Create a .env File for Environment Variables:
```
DB_HOST=yourdatabase.postgres.database.azure.com
DB_NAME=postgres
DB_USER=username@yourdatabase
DB_PASS=your_password
```
2. Load Environment Variables in Your Application and Run


## What's Included

- `app.py`: The main Flask application

## Lessons Learned

- Database Management: 
Integrating PostgreSQL with Streamlit for the Prompt Base app provided valuable lessons in database management, especially in the context of a cloud-hosted environment like Azure. It emphasized the significance of secure practices in handling database connections and credentials, such as using environment variables and SSL connections for security. This experience also underscored the importance of designing a scalable and normalized database schema to efficiently manage and query data.

- Error Handling and Debugging:
Throughout the development process, handling errors gracefully and debugging issues, especially related to database connections and operations, was crucial. Learning to interpret error messages accurately and researching solutions effectively were key skills honed during this project. This process underscored the importance of thorough testing and validation to catch and resolve issues early in the development cycle.

- Security Considerations: 
Implementing features such as user authentication or managing sensitive information taught the importance of security in web applications. While the Prompt Base app's scope might not extend to handling user accounts, the practice of securing database credentials and understanding potential security vulnerabilities in web applications was a valuable takeaway.

## Questions/Uncertainties

- What is the best practices for scaling the application. How can the app be optimized to handle a significant increase in user traffic and data? What are the potential bottlenecks, and how can they be addressed proactively?

- How to implement more advanced search features, such as fuzzy matching or searching within categories, poses questions about the best approach and tools to use. How can these features be implemented efficiently without compromising performance?

- While the Prompt Base app currently does not include user management, the addition of user-specific features would require implementing authentication and authorization. What are the best practices for integrating these features in a Streamlit app, and how can user data be secured effectively?

- What is the best practices for deploying and maintaining the Prompt Base app? What are the recommended strategies for continuous integration and continuous deployment (CI/CD)? How can the app be monitored effectively to ensure high availability and performance?

