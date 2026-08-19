# v0.1.0
# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }


from genlayer import *
import json


class AdjudicationEngine(gl.Contract):


    counter: u256
    cases: TreeMap[str,str]


    def __init__(self):

        self.counter = u256(0)
        self.cases = TreeMap[str,str]()



    def normalize_url(self,url):

        url = url.strip()

        if not url.startswith("http"):
            url = "https://" + url

        return url.split("#")[0]



    @gl.public.write
    def create_case(
        self,
        title:str,
        claim:str,
        criteria:str
    )->str:


        case_id = str(self.counter)

        self.counter += u256(1)


        case = {

            "id":case_id,

            "title":title,

            "claim":claim,

            "criteria":criteria,


            "status":"CREATED",

            "sources":[],

            "evidence":[],


            "verdict":"",

            "challenge":"",

            "challenged":False

        }


        self.cases[case_id]=json.dumps(case)


        return case_id




    @gl.public.write
    def add_sources(
        self,
        case_id:str,
        urls:list[str]
    )->str:


        if case_id not in self.cases:
            raise Exception("Case not found")


        case=json.loads(
            self.cases[case_id]
        )


        if case["status"]!="CREATED":
            raise Exception(
                "Sources already submitted"
            )



        normalized=[]


        for u in urls:

            normalized.append(
                self.normalize_url(u)
            )


        if len(normalized)<2:
            raise Exception(
                "At least two independent sources required"
            )



        case["sources"]=normalized

        case["status"]="SOURCES_SUBMITTED"


        self.cases[case_id]=json.dumps(case)


        return "sources added"




    @gl.public.write
    def adjudicate(
        self,
        case_id:str
    )->str:


        if case_id not in self.cases:
            raise Exception("Case not found")



        case=json.loads(
            self.cases[case_id]
        )


        if case["status"]!="SOURCES_SUBMITTED":
            raise Exception(
                "Invalid lifecycle state"
            )


        case["status"]="VERIFYING"



        evidence=[]



        for source in case["sources"]:


            def fetch():

                try:

                    data = gl.nondet.web.render(
                        source,
                        mode="text"
                    )


                    return {

                        "url":source,

                        "success":True,

                        "content":str(data)[:3000]

                    }


                except:


                    return {

                        "url":source,

                        "success":False,

                        "content":"FETCH_FAILED"

                    }



            result = gl.eq_principle.strict_eq(
                fetch
            )


            evidence.append(result)



        case["evidence"]=evidence



        prompt=f"""

You are a decentralized adjudicator.


CLAIM:

{case["claim"]}


CRITERIA:

{case["criteria"]}



SOURCES:

{json.dumps(evidence)}



Rules:


- Evaluate multiple sources together.
- Ignore failed fetches.
- Require consistent evidence.
- Do not trust URL existence alone.


Return only:


APPROVED: reason


or


REJECTED: reason

"""



        def judge():

            return gl.nondet.exec_prompt(
                prompt
            )



        verdict = gl.eq_principle.prompt_non_comparative(

            judge,

            task="Multi source adjudication",

            criteria=
            "Output must start with APPROVED: or REJECTED:"

        )



        verdict=str(verdict)



        case["verdict"]=verdict



        if verdict.startswith("APPROVED"):

            case["status"]="VERIFIED"

        else:

            case["status"]="REJECTED"



        self.cases[case_id]=json.dumps(case)



        return verdict




    @gl.public.write
    def challenge(
        self,
        case_id:str,
        reason:str
    )->str:


        if case_id not in self.cases:
            raise Exception("Case not found")


        case=json.loads(
            self.cases[case_id]
        )


        if case["status"] not in [
            "VERIFIED",
            "REJECTED"
        ]:

            raise Exception(
                "Case cannot be challenged"
            )



        case["challenged"]=True

        case["challenge"]=reason

        case["status"]="CHALLENGED"



        self.cases[case_id]=json.dumps(case)


        return "challenge submitted"




    @gl.public.view
    def get_case(
        self,
        case_id:str
    )->str:


        if case_id not in self.cases:

            return "not found"


        return self.cases[case_id]
