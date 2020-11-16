## Check your existing trial account

If you have already created a trial account in the past, we need to
ensure that have a subaccount in the **Europe (Frankfurt) - AWS**
region.
To confirm this, log in to your [Trial Account](https://cockpit.eu10.hana.ondemand.com/trial/)
and inspect the list of subaccounts.

You should have at least one subaccount where the **region** field is listed as
**Europe (Frankfurt) - AWS** as shown below:

![SCP Subaccount Europe (Frankfurt) -  AWS](images/scp_subaccount_frankfurt.png)

If you have a subaccount in the correct region, please proceed
to [Executing the Jupyter Notebook](./README.md#Executing-the-Jupyter-Notebook) and
skip the remaining steps below.

##### Subaccount in region other than Frankfurt - AWS

However, if your subaccount has a different region, please create a new subaccount
by clicking the "New Subaccount" button.

![SCP create new subaccount](images/scp_create_new_subaccount.png)

In the resulting popup, enter a **Display Name**,
select the **Europe (Frankfurt) - AWS** region and enter
a valid **subdomain** name. The name should be unique, so it is OK
to be creative here. Once you entered all details, click the
"Create" button.

![SCP new subaccount details](images/scp_new_subaccount_details.png)

Once the new subaccount is created, click on the name to enter the
subaccount.

![SCP enter new subaccount](images/scp_select_new_subaccount.png)

Click the "Enable Cloud Foundry" button.

![SCP enable Cloud Foundry](images/scp_enable_cloud_foundry.png)

In the resulting popup, accept the default org name and click the "Create" button.

![SCP Cloud Foundry org name](images/scp_cloud_foundry_org_name.png)

Once Cloud Foundry is available, click the "Create Space" button:

![SCP Create Space](images/scp_create_space.png)

Enter a name for the new Cloud Foundry space. "trial" is a good choice.
Then, click "Create".

![SCP Create Space Details](images/scp_create_space_details.png)

Once the space is created successfully, navigate back to your [main
trial global account](https://cockpit.eu10.hana.ondemand.com/trial/).

You are now ready to proceed to
[Executing the Jupyter Notebook](./README.md#Executing-the-Jupyter-Notebook).