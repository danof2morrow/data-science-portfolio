from google import genai
from getpass import getpass

api_key = getpass("Enter your Gemini API key: ")

client = genai.Client(api_key=api_key)

#Import packages
import json
#Figured out 10 cells later I needed this
from google import genai
from getpass import getpass
from IPython.display import Markdown, display

#Create the sample customer
customer = {
    "city": "Omaha",
    "state": "Nebraska",
    "organization_type": "Commercial fleet",
    "utility_provider": "Example Electric Utility",
    "planned_level2_chargers": 10,
    "estimated_project_cost": 150000,
    "expected_installation_year": 2027
}

display(customer)


#Create a sample utility program
utility_program = {
    "program_name": "Commercial EV Charging Rebate",
    "program_type": "Utility",
    "eligible_customer": "Nonresidential electric customers",
    "program_text": (
        "Eligible nonresidential customers may receive $2,000 per Level 2 charging port, "
        "up to 50% of eligible equipment and installation costs, with a maximum rebate of $20,000. "
        "Customers must receive program approval before purchasing equipment. "
        "Funding is subject to availability."
    ),
    "source": "Illustrative record for prompt testing"
}

#Create a sample government program
government_program = {
    "program_name": "Commercial Charging Infrastructure Grant",
    "program_type": "State",
    "eligible_customer": "Businesses operating in the state",
    "program_text": (
        "Eligible businesses may receive up to 40% of approved charging infrastructure costs, "
        "with a maximum award of $50,000. Applicants must operate in the state, submit an application "
        "before construction begins, and complete the project during the approved grant period."
    ),
    "source": "Illustrative record for prompt testing"
}

display(utility_program)
display(government_program)


#Import display tools
from IPython.display import Markdown, display

#Select the Gemini model
model_name = "gemini-3.5-flash-lite"

#Create a reusable API function
def run_prompt(prompt):
    response = client.models.generate_content(
        model=model_name,
        contents=prompt
    )
    return response.text

display(Markdown("**Output:** Reusable prompt function created."))

#Remove the utility provider for this experiment
customer_missing_utility = customer.copy()
customer_missing_utility.pop("utility_provider")

#Create the first prompt
prompt_1 = f'''
You are assisting a sales representative with a commercial fleet EV charging opportunity.

Customer information:
{json.dumps(customer_missing_utility, indent=2)}

Program information:
{json.dumps(utility_program, indent=2)}

Determine whether there is enough information to evaluate this program for the customer.
If important information is missing, ask only the questions needed before making an eligibility
or savings estimate. Do not assume missing facts.
'''

#Run the prompt
experiment_1 = run_prompt(prompt_1)

display(Markdown("**Output:**"))
display(Markdown(experiment_1))


#Create the second prompt
prompt_2 = f'''
You are assisting a sales representative with a commercial fleet EV charging opportunity.

Customer information:
{json.dumps(customer, indent=2)}

Utility program:
{json.dumps(utility_program, indent=2)}

Explain in plain language whether this program appears relevant to the customer.
Separate confirmed information from assumptions.
Identify any requirements that still need to be verified.
Do not state that the customer qualifies unless the supplied information clearly proves it.
Keep the response concise and useful for a sales conversation.
'''

#Run the prompt
experiment_2 = run_prompt(prompt_2)

display(Markdown("**Output:**"))
display(Markdown(experiment_2))


#Create the third prompt
prompt_3 = f'''
You are assisting a sales representative with a commercial fleet EV charging opportunity.

Customer information:
{json.dumps(customer, indent=2)}

Government program:
{json.dumps(government_program, indent=2)}

Summarize this program for the sales representative.
Separate confirmed eligibility requirements from assumptions.
Identify any location, timing, or application requirements.
List any customer information that still needs to be confirmed.
Keep the explanation short and practical.
'''

#Run the prompt
experiment_3 = run_prompt(prompt_3)

display(Markdown("**Output:**"))
display(Markdown(experiment_3))


#Create a rebate calculation function
def calculate_port_rebate(chargers, rebate_per_charger, project_cost, percent_limit, maximum_rebate):
    port_rebate = chargers * rebate_per_charger
    project_limit = project_cost * percent_limit
    return min(port_rebate, project_limit, maximum_rebate)

display(Markdown("**Output:** Rebate calculation function created."))


#Create the fourth prompt
prompt_4 = f'''
You are reviewing a commercial EV charging incentive.

Customer information:
{json.dumps(customer, indent=2)}

Program information:
{json.dumps(utility_program, indent=2)}

Determine whether enough information is available to calculate an estimated rebate.
If it is, identify the exact calculation rule and list the numeric inputs needed.
Do not perform the arithmetic.
If anything required is missing or ambiguous, explain what must be clarified.
'''

#Run the prompt
experiment_4 = run_prompt(prompt_4)

display(Markdown("**Model Output:**"))
display(Markdown(experiment_4))

#Calculate the rebate with Python
estimated_rebate = calculate_port_rebate(
    chargers=customer["planned_level2_chargers"],
    rebate_per_charger=2000,
    project_cost=customer["estimated_project_cost"],
    percent_limit=0.50,
    maximum_rebate=20000
)

display(Markdown(f"**Python Calculation Output:** Estimated rebate = ${estimated_rebate:,.0f}"))


#Create conflicting source information
source_a = {
    "source": "Source A",
    "program_text": "The program provides $2,000 per Level 2 charging port with a maximum rebate of $20,000."
}

source_b = {
    "source": "Source B",
    "program_text": "The program provides $1,500 per Level 2 charging port with a maximum rebate of $15,000."
}

#Create the fifth prompt
prompt_5 = f'''
You are reviewing two sources that describe the same commercial EV charging incentive.

{json.dumps(source_a, indent=2)}

{json.dumps(source_b, indent=2)}

Compare the two sources and identify every meaningful conflict.
Do not choose one source without evidence supporting that decision.
Explain what should be verified before the incentive is presented to a customer.
Keep the response concise.
'''

#Run the prompt
experiment_5 = run_prompt(prompt_5)

display(Markdown("**Output:**"))
display(Markdown(experiment_5))

