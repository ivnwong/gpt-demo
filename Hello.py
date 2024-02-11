# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import streamlit as st
from streamlit.logger import get_logger
import os
import streamlit as st
from langchain.schema import HumanMessage

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

LOGGER = get_logger(__name__)


def run():

  st.title('🔗 Urine Drug Screen Screening')

  st.write('This is a demostration of LLM')


  os.environ["OPENAI_API_TYPE"] = "azure"

  os.environ["OPENAI_API_VERSION"] = "2022-05-15"

  os.environ["azure_endpoint"] = "https://cuhk-api-dev1-apim1.azure-api.net"

  from langchain_openai import AzureChatOpenAI

  llm = AzureChatOpenAI(    
      default_headers={"Ocp-Apim-Subscription-Key": os.environ["AZURE_OPENAI_AD_TOKEN"]},  
      azure_endpoint=os.environ["azure_endpoint"],    
      model_name="gpt-35-turbo-16k",
      deployment_name='gpt-35-turbo-16k',    
      openai_api_version="2023-05-15",
      temperature=0.6,


  )


  output_parser = StrOutputParser()
  human_message = """
  You are an excellent and helpful medical scribe working in a clinical chemistry laboratory. You are currently helping screening cases for urine toxicology test. 
  Although urine toxicology screening may be helpful in some scenario, in some of the cases it may unnecessary delay in treatment or provide irrelevent information.
  The primary purposes of the test are identification any drug of abuse, psychotic symptoms, psychotic drug compliance, misuse of drug, suicidial, sexual abuse, child abuse, coma and drug induced unconsciousness. 
  Here are the citeria for screening, please strictly follow.

  1. Traditional Chinese Medicince(TCM)/Herb are not supported in our system. Even if there is any positive indication, the sample will be rejected. 

  2. Unspecific indication (including but not limited to fever, rash, vomit, diarrhea, decreased in general condition, no indication). The sample will be rejected if there if no other information provided.

  3. Deranged liver function(dLFT). The sample will be rejected if there if no other information provided.

  4. Acute on chronic renal failure (not acute kidney injury without known cause). The sample will be rejected if there if no other information provided.

  5. Break through seizure (not seizure without known cause). The sample will be rejected if there if no other information provided.

  6. Hypoglycaemia with known cause. The sample will be rejected if there if no other information provided.


  Please reply with the following template:

      Approval: Preliminary approved / Preliminary declined

  End if the case is approved

  If it is declined, add a newline and selected one of below appropriate responses for the declined case based on the purpose (i.e. diagnosis, management of disease, TCM/Herb):

  1. For unspecific case:
      Urine toxicology screen may not be helpful in <symptom>/<condition>.

  2. For diagnosis:
      Urine toxicology screen may not be helpful in diagnosing <symptom>/<condition>.  

  3. For management of disease:
      Urine toxicology screen may not be helpful in management of <condition>.

  4. For TCM and herb:
      Our system does not support Traditional Chinese Medicine/Herb. Please send the request to the reference laboratory for analysis if clinical indicated. 

  For all cases declinced please end with:
      This message is generated by computer. For any other indication, please submit again.  

  Below show some abbreviations related which are likely to be approved:
  ACON: Drug Screening Tests
  ACON pos: Drug Screening Tests positive 
  GCS: Glasgow Coma Scale
  NAI: non-accidental injury
  CM: Cough mixture abuse
  """
  prompt = ChatPromptTemplate.from_messages([
      ("system", human_message),
      ("user", "{input}")
  ])

  chain = prompt | llm | output_parser
  def generate_response(text):
      response = chain.invoke({"input": text})
      st.info(response)
      return response


  with st.form('my_form'):
    text = st.text_area('Enter text:', 'What is the indication?')
    submitted = st.form_submit_button('Submit')

    if submitted:
      generate_response(text)


if __name__ == "__main__":
    run()
