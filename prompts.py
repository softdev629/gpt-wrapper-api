SOURCE_VERIFY_PROMPT = """Can you review the content to ensure that all the information presented aligns 100% with the sources listed by the writer? Please follow these steps:
1.	Locate Sources:
o	Locate the section of the document under the subheading 'Links' or 'Sources' where URLs are provided.
o	If no sources are listed, respond with 'No sources provided' along with the statement 'You did not include any URLs for verification.'
2.	Validate Sources:
o	If sources are listed, extract and validate the URLs.
3.	Map Claims to Sources:
o	Map each claim in the article to the appropriate source from the list of URLs.
o	For each claim, verify whether the information in the article is fully supported by the content from the provided sources.
4.	Assess Source Support:
o	If all claims are supported by the sources, respond with 'Yes, sources check out' along with the statement 'All your claims are supported by the provided sources.'
o	If any claims are not supported by the sources or if a source does not match the content, respond with 'No, sources do not check out' and provide the exact number of unsupported claims, using the format 'Exactly [number] of your claims are not supported by the provided sources.'
5.	Detailed Breakdown of Issues:
o	If 'No, sources do not check out,' follow with a detailed breakdown listing the specific claims that are not supported, identifying the mismatched source(s), and explaining what corrections are needed for each unsupported claim.
o	The breakdown should include the following information for each unsupported claim:
1.	Claim: Clearly state the claim that is not supported by the source.
2.	Mismatched Source: Identify the specific source that does not match the claim.
3.	Suggested Fix: Provide suggestions on how you can correct the claim (e.g., rewording, finding a more appropriate source, or verifying the information).
Instruction: After you complete the analysis, output the final result along with a detailed breakdown, if necessary. Conduct a thorough analysis, taking the necessary time to evaluate the response, and then output the following:
•	Final Output: One of these three options:
1.	Yes, sources check out
-	Reason: 'All your claims are supported by the provided sources.'
-	Explanation: No further issues are found. No changes needed.
2.	No, sources do not check out
-	Reason: 'Exactly [number] of your claims are not supported by the provided sources.'
-	Detailed Breakdown:
-	Claim 1: '[Insert unsupported claim]' is not backed by the source '[Insert mismatched URL].' Consider rewording the claim or finding a more relevant source.
-	Claim 2: '[Insert unsupported claim]' contains information that differs from the content in '[Insert mismatched URL].' Verify the claim against the source or update it.
-	(Continue for each unsupported claim)
3.	No sources provided
-	Reason: 'You did not include any URLs for verification.'
-	Explanation: The document does not contain any URLs for verification. Consider adding reliable sources to back up your claims.
Important: Always provide a detailed breakdown for 'No, sources do not check out' responses, specifying exactly which of your claims are unsupported, which sources are mismatched, and how to fix the issues. For 'No sources provided,' suggest adding relevant sources for claims verification.
"""

DETAIL_VERIFY_PROMPT = """Can you review this script to determine if the content is detailed enough to fully address and solve the reader's problem while remaining brief and to the point? Please follow these steps:
1.	Identify the Core Problem:
o	Identify the core problem or question your script is addressing.
2.	Evaluate the Solution:
o	Evaluate whether the solution you provided is complete and includes all necessary steps to solve the problem.
3.	Check for Relevance:
o	Check that all details in your script are relevant to the solution and avoid unnecessary or unrelated information.
4.	Assess the Level of Detail:
o	Assess whether the level of detail is appropriate, ensuring that the reader can understand and follow the steps without confusion.
5.	Avoid Unnecessary Repetition:
o	Determine if your script avoids unnecessary repetition and remains brief and to the point.
6.	Account for Variations/Edge Cases:
o	Verify if your content accounts for common variations or edge cases related to the problem.
7.	Audience Appropriateness:
o	Ensure the level of detail in your script matches the expectations and knowledge level of the intended audience.
Provide Suggestions for Fixing Issues:
•	If the response is 'Not detailed enough,' provide specific suggestions to help you improve the content. Break down exactly what needs to be done, such as adding more steps, removing irrelevant details, or clarifying ambiguous points.
Instruction:
Please provide the final Possible Output based on the steps above. Conduct a thorough analysis, taking the necessary time to evaluate the response, and then output only one of the following:
1.	Detailed enough
o	Reason: 'The content fully solves the problem and remains brief and to the point.'
o	Explanation: No further improvements are needed.
2.	Not detailed enough
o	Reason: 'The content has Exactly [number] ambiguities and Exactly [number] areas that lack detail or are irrelevant.'
o	Detailed Breakdown of Fixes Needed:
-	Ambiguities: Clearly list each ambiguity found and explain how you can clarify it (e.g., 'The step explaining how to reset the system is unclear; include more detail about the specific options in the settings menu.').
-	Lack of Detail: Identify areas that need more detail (e.g., 'The instructions on how to back up data are too vague; add a step-by-step process explaining how to access the backup options.').
-	Irrelevant Information: Specify which information is unnecessary and should be removed (e.g., 'The section about the history of the tool is irrelevant to solving the problem and should be removed.').
Fix Suggestions:
For each issue, provide a clear action you should take to improve the script, such as:
•	Add More Steps: 'The solution is missing key steps in the process. You should add [specific steps] to ensure the reader can follow along.'
•	Remove Unnecessary Information: 'There is irrelevant information in the section about [topic], which doesn't contribute to solving the problem. Consider removing it to keep the content focused.'
•	Clarify Ambiguities: 'Some steps are not clear enough for the intended audience. You should clarify [specific points] to avoid confusion.'
Important:
Always include a detailed breakdown when the output is 'Not detailed enough,' specifying exactly what areas need to be improved and how you can fix them. For 'Detailed enough,' provide confirmation that no further changes are needed.
"""

FACTUAL_VERIFY_PROMPT = """Can you review this script to verify that all the information is 100% factual? Please follow these steps:
1.	Break the Script into Claims:
o	Break your script into individual factual claims or statements.
2.	Cross-Check Claims:
o	For each claim, first cross-check the information against the sources you provided (if available). If the sources are absent or do not seem credible, cross-check the claims against reliable and trustworthy online sources.
3.	Check Consistency:
o	Ensure that the facts are consistent with each other within your script and are logical in context.
4.	Flag Ambiguities:
o	If any claim is ambiguous, unclear, or cannot be verified, flag it as requiring further clarification.
5.	Knowledge Cutoff:
o	If a claim references information beyond the system's knowledge cutoff, respond with 'knowledge cutoff reached.'
6.	Verify Accuracy:
o	If all claims are verified and accurate, respond with 'Yes, it's all factual.'
o	If any claims are not accurate or cannot be verified, respond with 'No, there are inaccuracies' and specify the exact number of inaccuracies, using the format 'Exactly [number] claims are inaccurate.'
Provide Suggestions for Fixing Inaccuracies:
•	If the response is 'No, there are inaccuracies,' provide a detailed breakdown for you, listing each inaccurate claim and offering specific suggestions on how to correct it (e.g., updating information, removing unsupported claims, or finding more reliable sources).
Instruction:
Please provide the final Possible Output based on the steps above. Conduct a thorough analysis, taking the necessary time to evaluate the response, and then output only one of the following:
1.	Yes, it's all factual
o	Reason: 'All claims in your script are accurate and verified.'
o	Explanation: No further changes are required, and the content is factually sound.
2.	No, there are inaccuracies
o	Reason: 'Exactly [number] claims are inaccurate.'
o	Detailed Breakdown of Fixes Needed:
-	Inaccuracy 1: '[Insert inaccurate claim]' is factually incorrect based on [insert source or reasoning]. Consider revising the claim to reflect [insert correct information].
-	Inaccuracy 2: '[Insert inaccurate claim]' does not match the data from [insert source]. Update the claim with information from a more reliable or recent source.
-	(Continue for each inaccurate claim)
o	Fix Suggestions:
-	Update Facts: 'For [specific claim], update the information with the correct data from a reliable source such as [insert source].'
-	Remove Unsupported Claims: 'The claim about [specific topic] is not supported by any credible sources. Consider removing it or finding a reliable source to back it up.'
-	Clarify Ambiguous Statements: 'The statement regarding [specific topic] is too vague and needs clarification. Provide more detail or context to ensure accuracy.'
3.	Knowledge cutoff reached
o	Reason: 'Some claims reference information beyond the system's knowledge cutoff.'
o	Explanation: The claims could not be verified because they involve information beyond the system's current knowledge. You may need to fact-check those claims using up-to-date sources.
Important:
•	Always provide a detailed breakdown for 'No, there are inaccuracies' responses, specifying which claims are inaccurate and what needs to be corrected.
•	For 'Yes, it's all factual,' confirm that no further changes are needed.
•	For 'Knowledge cutoff reached,' clearly state that the information exceeds the system's knowledge and recommend further fact-checking.
"""

TECH_VERIFY_PROMPT = """Can you review this article for potential technical inaccuracies, inconsistencies, safety risks, and factual accuracy? Additionally, verify that the claims are supported by credible sources, both from the writer and external references. Please follow these steps:
________________________________________
1. Determine Presence of Technical Details:
•	First, assess whether the article contains technical details, such as specifications, ratings, measurements, safety instructions, or usage guidelines.
o	If no technical content is present, respond with 'No technical details found' along with the statement, 'The article does not contain any technical information that requires verification.'
________________________________________
2. Identify Critical Technical Information (if applicable):
•	If technical details are present, break the article into sections and identify key technical details, such as specifications, ratings, measurements, safety instructions, or usage guidelines. Consider the following technical aspects:
o	Specifications and Ratings
o	Measurements and Units
o	Tolerances and Limits
o	Safety Instructions and Warnings
o	Usage Guidelines and Best Practices
o	Component Descriptions and Functions
o	Process and Step-by-Step Instructions
o	Materials and Durability Information
o	Energy and Power Consumption
o	Operating Conditions and Environmental Factors
o	Maintenance and Repair Information
o	Troubleshooting and Diagnostics
o	Compatibility and Interoperability
________________________________________
3. Cross-Check Technical Accuracy:
•	For each identified technical detail, cross-check it against reliable and established standards, manufacturer guidelines, or trusted sources in the relevant field. Ensure that:
o	Specifications, ratings, or measurements align with standard practices.
o	Safety recommendations and usage guidelines are correct and not misleading.
o	Any numerical values match industry norms or manufacturer specs.
________________________________________
4. Verify Sources and Cross-Check Information:
•	Locate and Verify Provided Sources:
o	Identify the sources provided by the writer (e.g., under a 'Sources' or 'Links' section). Check if these sources are credible and directly support the claims in the article.
o	Ensure that each key technical detail is supported by an appropriate source from the writer's list. If any claims are unsupported or mismatched, flag them for correction.
•	Cross-Check with Reliable Online Sources:
o	If the writer’s sources are absent, incomplete, or not credible, verify the claims against reliable and trustworthy online sources, such as official documentation, industry-standard references, or academic publications.
o	Ensure that the technical details are consistent with current best practices and factual information found in authoritative sources.
•	Assess Source Alignment:
o	If all technical claims are fully supported by the writer's sources or external credible sources, respond with 'Yes, sources check out.'
o	If any claims are not supported, respond with 'No, sources do not check out' and list the specific unsupported claims.
________________________________________
5. Assess the Safety Risks:
•	Evaluate potential safety risks associated with incorrect technical information. For each detail, consider:
o	Could misleading or incorrect details lead to harm, equipment damage, or safety hazards (e.g., fire risk, mechanical failure)?
o	Does the article explain why correct specifications (e.g., proper fuse ratings) are crucial for avoiding risks?
________________________________________
6. Check for Contradictions or Inconsistencies:
•	Ensure there are no contradictions within the article. Verify that:
o	Information is consistent throughout, with no conflicting technical advice.
o	Instructions and explanations follow a logical, coherent sequence.
________________________________________
7. Evaluate Clarity for the Reader:
•	Assess whether technical details are explained clearly for the intended audience. Consider:
o	Are technical terms and concepts explained where necessary?
o	Could any part of the article confuse the reader or lead to misinterpretation?
________________________________________
8. Flag Potential Errors or Ambiguities:
•	Identify any areas where technical information could be misunderstood or misapplied. If errors or ambiguous sections are found, flag them for correction.
________________________________________
9. Compare Against Industry Standards:
•	Compare key technical claims and safety recommendations against relevant industry standards. If the article deviates from these standards, suggest corrections to bring it in line with best practices.
________________________________________
Provide Suggestions for Fixing Issues:
•	If inaccuracies, inconsistencies, unsupported claims, or safety risks are found, provide a detailed breakdown, offering suggestions on how to fix them. For example:
o	Technical Accuracy Issue: '[Insert inaccurate technical detail]' is incorrect based on [insert source or standard]. Consider revising it to '[insert corrected detail].'
o	Source Issue: '[Insert claim]' is not supported by any credible source. Either remove the claim or find a reputable source to back it up.
o	Safety Risk: '[Insert detail]' poses a safety risk (e.g., fire hazard). Add a warning to ensure proper usage.
o	Clarity Issue: '[Insert technical explanation]' could confuse readers. Provide more context or explanation to clarify.
________________________________________
Instruction:
Please conduct a thorough analysis and output one of the following based on the technical accuracy and source verification of the article:
1.	No technical details found:
o	Reason: 'The article does not contain any technical information that requires verification.'
2.	Technically Accurate and Supported by Sources:
o	Reason: 'All technical details are accurate and supported by credible sources.'
o	Explanation: No revisions needed; the article is technically sound and properly sourced.
3.	Technical Issues Identified:
o	Reason: 'Exactly [number] technical inaccuracies or inconsistencies found.'
o	Detailed Breakdown of Fixes Needed:
	Inaccuracy 1: '[Insert inaccurate technical detail]' is incorrect. Correct as '[insert corrected detail].'
	Safety Risk 1: '[Insert safety issue]' poses a hazard. Correct this to '[insert corrected safety detail].'
4.	Unsupported Claims or Mismatched Sources:
o	Reason: 'Exactly [number] claims are not supported by the sources provided or external credible sources.'
o	Detailed Breakdown of Fixes Needed:
	Unsupported Claim 1: '[Insert claim]' is not backed by [insert source]. Either find a reliable source or remove the claim from the article.
5.	Ambiguities or Misleading Information:
o	Reason: 'Exactly [number] areas are ambiguous or could mislead the reader.'
o	Detailed Breakdown of Fixes Needed:
	Ambiguity 1: '[Insert ambiguous section]' needs clarification. Suggest rewording as '[insert correction].'
6.	Critical Safety Risk Identified:
o	Reason: 'A critical safety risk was found related to [insert issue].'
o	Explanation: This must be corrected immediately to prevent hazards like overheating or mechanical failure. Correct as '[insert fix].'
________________________________________
Important:
Always provide a detailed breakdown for 'Technical Issues Identified,' 'Unsupported Claims,' and 'Ambiguities or Misleading Information' responses, specifying the exact issues and how they can be resolved. For 'Critical Safety Risk,' flag the issue for immediate correction.
"""