from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://165.227.93.171:3000",
    "https://verifycontent.cc/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def main():
    return {"message": "Hello World"}


class ISigninRequest(BaseModel):
    email: str
    password: str


@app.post("/api/signin")
async def signin_handler(req: ISigninRequest):
    if req.password == "friendship":
        return {"logged_in": True}
    return {"logged_in": False}


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.post("/api/verify/source")
async def verify_source_handler(text: str = Body(embed=True)):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """Can you review the content to ensure that all the information presented aligns 100% with the sources listed by the writer? Please follow these steps:
1.	Locate Sources:
o	Locate the section of the document under the subheading 'Links' or 'Sources' where URLs are provided.
o	If no sources are listed, respond with 'No sources provided' along with the statement 'There are no URLs listed in the document for verification.'
2.	Validate Sources:
o	If sources are listed, extract and validate the URLs.
3.	Map Claims to Sources:
o	Map each claim in the article to the appropriate source from the list of URLs.
o	For each claim, verify whether the information in the article is fully supported by the content from the provided sources.
4.	Assess Source Support:
o	If all claims are supported by the sources, respond with 'Yes, sources check out' along with the statement 'All claims are supported by the provided sources.'
o	If any claims are not supported by the sources or if a source does not match the content, respond with 'No, sources do not check out' and provide the exact number of unsupported claims, using the format 'Exactly [number] claims are not supported by the provided sources.'
5.	Detailed Breakdown of Issues:
o	If 'No, sources do not check out,' follow with a detailed breakdown listing the specific claims that are not supported, identifying the mismatched source(s), and explaining what corrections are needed for each unsupported claim.
o	The breakdown should include the following information for each unsupported claim:
1.	Claim: Clearly state the claim that is not supported by the source.
2.	Mismatched Source: Identify the specific source that does not match the claim.
3.	Suggested Fix: Provide suggestions on how the writer can correct the claim (e.g., rewording, finding a more appropriate source, or verifying the information).
Instruction: After you complete the analysis, output the final result along with a detailed breakdown, if necessary. Conduct a thorough analysis, taking the necessary time to evaluate the response, and then output the following:
•	Final Output: One of these three options:
1.	Yes, sources check out
-	Reason: 'All claims are supported by the provided sources.'
-	Explanation: No further issues are found. No changes needed.
2.	No, sources do not check out
-	Reason: 'Exactly [number] claims are not supported by the provided sources.'
-	Detailed Breakdown:
-	Claim 1: '[Insert unsupported claim]' is not backed by the source '[Insert mismatched URL].' Consider rewording the claim or finding a more relevant source.
-	Claim 2: '[Insert unsupported claim]' contains information that differs from the content in '[Insert mismatched URL].' Verify the claim against the source or update it.
-	(Continue for each unsupported claim)
3.	No sources provided
-	Reason: 'There are no URLs listed in the document for verification.'
-	Explanation: The document does not contain any URLs for verification. The writer should consider adding reliable sources to back up their claims.
Important: Always provide a detailed breakdown for 'No, sources do not check out' responses, specifying exactly which claims are unsupported, which sources are mismatched, and how to fix the issues. For 'No sources provided,' suggest adding relevant sources for claims verification.
""",
            },
            {
                "role": "user",
                "content": f"Review the following content as specified in the system.\n\n<content>{text}</content>",
            },
        ],
    )
    return {"result": completion.choices[0].message.content}


@app.post("/api/verify/detail")
async def verify_detail_handler(text: str = Body(embed=True)):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """Can you review this script to determine if the content is detailed enough to fully address and solve the reader's problem while remaining brief and to the point? Please follow these steps:
1.	Identify the Core Problem:
o	Identify the core problem or question the script is addressing.
2.	Evaluate the Solution:
o	Evaluate whether the solution provided is complete and includes all necessary steps to solve the problem.
3.	Check for Relevance:
o	Check that all details are relevant to the solution and avoid unnecessary or unrelated information.
4.	Assess the Level of Detail:
o	Assess whether the level of detail is appropriate, ensuring that the reader can understand and follow the steps without confusion.
5.	Avoid Unnecessary Repetition:
o	Determine if the script avoids unnecessary repetition and remains brief and to the point.
6.	Account for Variations/Edge Cases:
o	Verify if the content accounts for common variations or edge cases related to the problem.
7.	Audience Appropriateness:
o	Ensure the level of detail matches the expectations and knowledge level of the intended audience.
Provide Suggestions for Fixing Issues:
•	If the response is 'Not detailed enough,' provide specific suggestions to help the writer improve their content. Break down exactly what needs to be done, such as adding more steps, removing irrelevant details, or clarifying ambiguous points.
Instruction: Please provide the final Possible Output based on the steps above. Conduct a thorough analysis, taking the necessary time to evaluate the response, and then output only one of the following:
1.	Detailed enough
o	Reason: 'The content fully solves the problem and remains brief and to the point.'
o	Explanation: No further improvements are needed.
2.	Not detailed enough
o	Reason: 'The content has Exactly [number] ambiguities and Exactly [number] areas that lack detail or are irrelevant.'
o	Detailed Breakdown of Fixes Needed:
	Ambiguities: Clearly list each ambiguity found and explain how the writer can clarify it (e.g., 'The step explaining how to reset the system is unclear; include more detail about the specific options in the settings menu.').
	Lack of Detail: Identify areas that need more detail (e.g., 'The instructions on how to back up data are too vague; add a step-by-step process explaining how to access the backup options.').
	Irrelevant Information: Specify which information is unnecessary and should be removed (e.g., 'The section about the history of the tool is irrelevant to solving the problem and should be removed.').
Fix Suggestions:
For each issue, provide a clear action the writer should take to improve the script, such as:
•	Add More Steps: 'The solution is missing key steps in the process. You should add [specific steps] to ensure the reader can follow along.'
•	Remove Unnecessary Information: 'There is irrelevant information in the section about [topic], which doesn't contribute to solving the problem. Consider removing it to keep the content focused.'
•	Clarify Ambiguities: 'Some steps are not clear enough for the intended audience. You should clarify [specific points] to avoid confusion.'
Important: Always include a detailed breakdown when the output is 'Not detailed enough,' specifying exactly what areas need to be improved and how the writer can fix them. For 'Detailed enough,' provide confirmation that no further changes are needed.
""",
            },
            {
                "role": "user",
                "content": f"Review the following content as specified in the system.\n\n<content>{text}</content>",
            },
        ],
    )
    return {"result": completion.choices[0].message.content}


@app.post("/api/verify/factual")
async def verify_factual_handler(text: str = Body(embed=True)):
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": """Can you review this script to verify that all the information is 100% factual? Please follow these steps:
1.	Break the Script into Claims:
o	Break the script into individual factual claims or statements.
2.	Cross-Check Claims:
o	For each claim, first cross-check the information against the sources provided by the writer (if available). If the sources are absent or do not seem credible, cross-check the claims against reliable and trustworthy online sources.
3.	Check Consistency:
o	Ensure that the facts are consistent with each other within the script and logical in context.
4.	Flag Ambiguities:
o	If any claim is ambiguous, unclear, or cannot be verified, flag it as requiring further clarification.
5.	Knowledge Cutoff:
o	If a claim references information beyond your knowledge cutoff, respond with 'knowledge cutoff reached.'
6.	Verify Accuracy:
o	If all claims are verified and accurate, respond with 'Yes, it's all factual.'
o	If any claims are not accurate or cannot be verified, respond with 'No, there are inaccuracies' and specify the exact number of inaccuracies, using the format 'Exactly [number] claims are inaccurate.'
Provide Suggestions for Fixing Inaccuracies:
•	If the response is 'No, there are inaccuracies,' provide a detailed breakdown for the writer, listing each inaccurate claim and offering specific suggestions on how to correct it (e.g., updating information, removing unsupported claims, or finding more reliable sources).
Instruction: Please provide the final Possible Output based on the steps above. Conduct a thorough analysis, taking the necessary time to evaluate the response, and then output only one of the following:
1.	Yes, it's all factual
o	Reason: 'All claims in the script are accurate and verified.'
o	Explanation: No further changes are required, and the content is factually sound.
2.	No, there are inaccuracies
o	Reason: 'Exactly [number] claims are inaccurate.'
o	Detailed Breakdown of Fixes Needed:
	Inaccuracy 1: '[Insert inaccurate claim]' is factually incorrect based on [insert source or reasoning]. Consider revising the claim to reflect [insert correct information].
	Inaccuracy 2: '[Insert inaccurate claim]' does not match the data from [insert source]. Update the claim with information from a more reliable or recent source.
	(Continue for each inaccurate claim)
o	Fix Suggestions:
	Update Facts: 'For [specific claim], update the information with the correct data from a reliable source such as [insert source].'
	Remove Unsupported Claims: 'The claim about [specific topic] is not supported by any credible sources. Consider removing it or finding a reliable source to back it up.'
	Clarify Ambiguous Statements: 'The statement regarding [specific topic] is too vague and needs clarification. Provide more detail or context to ensure accuracy.'
3.	Knowledge cutoff reached
o	Reason: 'Some claims reference information beyond the knowledge cutoff.'
o	Explanation: The claims could not be verified because they involve information beyond the Systems current knowledge. Further fact-checking may be required by the writer using up-to-date sources.
Important:
•	Always provide a detailed breakdown for 'No, there are inaccuracies' responses, specifying which claims are inaccurate and what needs to be corrected.
•	For 'Yes, it's all factual,' confirm that no further changes are needed.
•	For 'Knowledge cutoff reached,' clearly state that the information exceeds the Systems knowledge and recommend further fact-checking.
""",
            },
            {
                "role": "user",
                "content": f"Review the following content as specified in the system.\n\n<content>{text}</content>",
            },
        ],
    )
    return {"result": completion.choices[0].message.content}
