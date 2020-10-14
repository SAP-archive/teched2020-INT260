# Exercise 2.1 - Provision instance for Service Ticket Intelligence

In this part of the exercise, we will see how to create a service instance of Service Ticket Intelligence in SAP Cloud Platform Cockpit and obtain the `sti_service_url`, `uaa.url`, `client_id` and `client_secret` which will then be used to authorize and communicate with Service Ticket Intelligence. 

## Steps

### Access SAP Cloud Platform Cockpit

1. In your web browser, navigate to the [SAP Cloud Platform trial cockpit](https://cockpit.hanatrial.ondemand.com/).
   ![](../images/1.1.png)

1. Navigate to the trial global account by clicking **Enter Your Trial Account**.
   1. If this is your first time accessing your trial account, you’ll have to configure your account by choosing a region.
   1. Please select **Europe (Frankfurt)**. Your user profile will be set up for you automatically.
   1. Choose **Continue**.
      ![](../images-sti/1.2.png)

1. From your global account page, choose the `trial` tile to access your subaccount.
   ![](../images-sti/1.3.png)

### Check entitlements
To try out Service Ticket Intelligence, you need to make sure that your account is properly configured.

1. On the navigation sidebar, click **Entitlements** to see a list of all eligible services. You are entitled to use every service in this list according to the assigned service plan.

1. Search for **Service Ticket Intelligence Trial**. If you find the service in the list, you are entitled to use it. Now you can set this step to **Done** and proceed with the next step.
   ![](../images-sti/1.4.png) 

1. If you do not find the service in your list, proceed as follows:
   1. Click **Configure Entitlements**.
      ![](../images-sti/1.5.png)
   1. Click **Add Service Plans** to add service plans to your entitlements.
      ![](../images-sti/1.6.png)
   1. Select **Service Ticket Intelligence Trial**, and choose the **standard** service plan. Click **Add 1 Service Plan**.
      ![](../images-sti/1.7.png)
   1. **Save** your entitlement changes. You are now entitled to use the service and to create instances of the service.
      ![](../images-sti/1.8.png)

### Access space
All applications and services live in spaces. By default, trial accounts only have the **dev** space available.

1. To access your spaces, click **Spaces** on the navigation sidebar and select the **dev** space to open it.
   ![](../images-sti/1.9.png)

1. In this space you will create your service instance.

### Access service via Service Marketplace
The **Service Marketplace** is where you find the available services on SAP Cloud Platform.

1. To access it, click **Service Marketplace** on the navigation sidebar.
   ![](../images-sti/1.10.png)

1. Next, search for **Service Ticket Intelligence**. Click the tile named `service-ticket-intelligence-trial` to access the service.
   ![](../images-sti/1.11.png)

### Create service instance
You will now create an instance of your service.

1. Click **Create Instance** to start the creation dialog.
   ![](../images-sti/1.12.png)

1. In the dialog, leave the default value for the service and the service plan. Enter a name for your new instance as `sti-demo` and click **Create Instance** to skip the other steps and create the instance.
   ![](../images-sti/1.13.png)

1. In the following dialog, click on **View Instance** to be navigated to the list of your service instances.
   ![](../images-sti/1.14.png)

You have successfully created a service instance for Service Ticket Intelligence.

### Create service keys
You are now able to create service keys for your new service instance. Service keys are used to generate credentials to enable apps to access and communicate with the service instance.

1. Click the navigation arrow to open the details of your service instance. Then, click the dots to open the menu and select **Create Service Key**.
   ![](../images-sti/1.15.png)

1. In the dialog, enter `sti-demo-key` as the name of your service key. Click **Create** to create the service key.
   ![](../images-sti/1.16.png)
   
You have successfully created service keys for your service instance. You can now either view the service key in the browser or download it.
![](../images-sti/1.17.png)

### Record down service keys
Note down the `sti_service_url`, `uaa.url`, `uaa.clientid` and `uaa.clientsecret` as these will be used to obtain the bearer token, which should be provided when connecting to STI in the following exercise.
