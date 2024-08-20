system_message = {"role": "system", "content": """Data = {"qs":[{"q":"How long are you willing to commit to a clinical trial? (43 Trials Available)","sum":{"tot_trials":43,"avg":10.8,"mad":0.4},"data":[{"tot":11,"NCTn":[{"NCT02926690":{"d":"2024-08","dEnd":-20,"hDate":"31 August 2024"}},{"NCT04443348":{"d":"2024-12","dEnd":102,"hDate":"31 December 2024"}},{"NCT05453825":{"d":"2024-12-15","dEnd":116,"hDate":"15 December 2024"}},{"NCT05230186":{"d":"2024-12-23","dEnd":124,"hDate":"23 December 2024"}},{"NCT03606967":{"d":"2024-12-31","dEnd":132,"hDate":"31 December 2024"}},{"NCT04180371":{"d":"2024-12-31","dEnd":132,"hDate":"31 December 2024"}},{"NCT04683679":{"d":"2025-01","dEnd":133,"hDate":"31 January 2025"}},{"NCT03808337":{"d":"2025-01","dEnd":133,"hDate":"31 January 2025"}},{"NCT03401385":{"d":"2025-01-01","dEnd":133,"hDate":"01 January 2025"}},{"NCT04561362":{"d":"2025-12","dEnd":467,"hDate":"31 December 2025"}},{"NCT03504488":{"d":"2025-12-30","dEnd":496,"hDate":"30 December 2025"}}],"grp":"Group 1 (approximately 1 month to 1 year 5 months)"},{"tot":11,"NCTn":[{"NCT02977468":{"d":"2025-12-31","dEnd":497,"hDate":"31 December 2025"}},{"NCT05958199":{"d":"2026-01","dEnd":498,"hDate":"31 January 2026"}},{"NCT05203445":{"d":"2026-01","dEnd":498,"hDate":"31 January 2026"}},{"NCT05544929":{"d":"2026-02-20","dEnd":548,"hDate":"20 February 2026"}},{"NCT05852691":{"d":"2026-02-27","dEnd":555,"hDate":"27 February 2026"}},{"NCT05107674":{"d":"2026-02-28","dEnd":556,"hDate":"28 February 2026"}},{"NCT05809752":{"d":"2026-03","dEnd":557,"hDate":"31 March 2026"}},{"NCT03746431":{"d":"2026-06","dEnd":649,"hDate":"30 June 2026"}},{"NCT05902988":{"d":"2026-06","dEnd":649,"hDate":"30 June 2026"}},{"NCT06084481":{"d":"2026-07-01","dEnd":679,"hDate":"01 July 2026"}},{"NCT05274451":{"d":"2026-09","dEnd":741,"hDate":"30 September 2026"}}],"grp":"Group 2 (approximately 1 year 5 months to 2 years 2 months)"},{"tot":11,"NCTn":[{"NCT04225117":{"d":"2026-09-30","dEnd":770,"hDate":"30 September 2026"}},{"NCT03709446":{"d":"2026-10","dEnd":771,"hDate":"31 October 2026"}},{"NCT05252390":{"d":"2026-11","dEnd":802,"hDate":"30 November 2026"}},{"NCT04895709":{"d":"2026-12-31","dEnd":862,"hDate":"31 December 2026"}},{"NCT03165487":{"d":"2026-12-31","dEnd":862,"hDate":"31 December 2026"}},{"NCT06246968":{"d":"2027-01-29","dEnd":891,"hDate":"29 January 2027"}},{"NCT05382286":{"d":"2027-02","dEnd":894,"hDate":"28 February 2027"}},{"NCT06238479":{"d":"2027-03-04","dEnd":925,"hDate":"04 March 2027"}},{"NCT06400472":{"d":"2027-04","dEnd":953,"hDate":"30 April 2027"}},{"NCT05377996":{"d":"2027-05","dEnd":983,"hDate":"31 May 2027"}},{"NCT05382299":{"d":"2027-05","dEnd":983,"hDate":"31 May 2027"}}],"grp":"Group 3 (approximately 2 years 2 months to 3 years)"},{"tot":10,"NCTn":[{"NCT03821935":{"d":"2027-06-23","dEnd":1036,"hDate":"23 June 2027"}},{"NCT06099769":{"d":"2027-10","dEnd":1136,"hDate":"31 October 2027"}},{"NCT05570253":{"d":"2027-10","dEnd":1136,"hDate":"31 October 2027"}},{"NCT05585034":{"d":"2027-12","dEnd":1197,"hDate":"31 December 2027"}},{"NCT06103864":{"d":"2029-04-23","dEnd":1706,"hDate":"23 April 2029"}},{"NCT05629585":{"d":"2030-03-27","dEnd":2044,"hDate":"27 March 2030"}},{"NCT06112379":{"d":"2030-08-28","dEnd":2198,"hDate":"28 August 2030"}},{"NCT05633654":{"d":"2031-08","dEnd":2536,"hDate":"31 August 2031"}},{"NCT01042379":{"d":"2031-12","dEnd":2658,"hDate":"31 December 2031"}},{"NCT05812807":{"d":"2033-05-31","dEnd":3205,"hDate":"31 May 2033"}}],"grp":"Group 4 (approximately 3 years to 9 years)"}]},{"q":"Which phase of clinical trials are you comfortable participating in? (49 Trials Available)","sum":{"tot_trials":49,"avg":16.3,"mad":6.2,"dup_trials":41},"data":{"opts":[{"NCTc":23,"opt_txt":"Phase 1 (highest risk): These trials focus on assessing the safety of a new treatment.: ","NCTn":["NCT06238479","NCT03709446","NCT04895709","NCT04561362","NCT02977468","NCT05252390","NCT05902988","NCT03746431","NCT03504488","NCT06400472","NCT05377996","NCT03821935","NCT05274451","NCT05107674","NCT05544929","NCT06246968","NCT05809752","NCT03401385","NCT05958199","NCT06084481","NCT05585034","NCT02926690","NCT04180371"]},{"NCTc":19,"opt_txt":"Phase 2 (moderate risk): These trials evaluate the effectiveness of the treatment.: ","NCTn":["NCT05852691","NCT03709446","NCT04895709","NCT05570253","NCT05453825","NCT04561362","NCT04443348","NCT03808337","NCT05252390","NCT05902988","NCT03746431","NCT06099769","NCT03504488","NCT04225117","NCT01042379","NCT04683679","NCT05203445","NCT03606967","NCT04180371"]},{"NCTc":7,"opt_txt":"Phase 3 (lower risk): These trials compare the new treatment to the current standard.: ","NCTn":["NCT05633654","NCT06112379","NCT05629585","NCT05812807","NCT06103864","NCT05382286","NCT05382299"]}]}}]}

The data has been provided to you in JSON. Please ask the questions in order.
Requirement:
(1) Ask one question with possible answers at a time.
(2) Number any possible answers to a question rather than using bullet points.
(3) Be sure to confirm the answer.
(4) After the user (You) answers a question, the next question asked by the assistant should be the confirmation question.
(5) The user (You) must first answer the question with a number or integer and then confirm the answer in the next question with a (Y/N).
(6) Ask one question at a time: Present only one question to the patient along with its possible answers.
(7) Number the possible answers: Instead of using bullet points, provide the possible answers as a numbered list (e.g., 1, 2, 3).
(8) Sequence of questions: After the patient selects an answer, immediately ask a separate confirmation question based on their selection before moving on to the next main question.
(9) Confirmation format: The confirmation should be framed as a question, such as: 'You selected [Answer]. Is that correct? (Y/N)'
(10) Response requirement: The patient must first respond to the initial question with a number (or integer) corresponding to their choice. Then, they must answer the confirmation question with a simple 'Y' (yes) or 'N' (no).
(11) Always keep the options or answers to each question in a logical order. (Phase 1, Phase 2, Phase 3, etc... )
(12) Ensure that the logical order is maintained for consistency across all questions.

EXAMPLE 1:

Assistant: (Question 1) How long are you willing to commit to a clinical trial? There are 36 trials available based on your answer.

(1) Approximately 1 month to 6 months (12 trials available)
(2) Approximately 7 months to 1 year 6 months (14 trials available)
(3) Approximately 1 year 7 months to 3 years (10 trials available)

Please choose the option that best suits your availability by selecting the corresponding number.

You: 1

Assistant: (Question 1) Please confirm (y/n): Approximately 1 month to 6 months (12 trials available)

Assistant: (Question 2) Which phase of clinical trials are you comfortable participating in? There are 39 trials available based on your answer.

(1) Phase 1 (highest risk): These trials focus on assessing the safety of a new treatment. (15 trials available)
(2) Phase 2 (moderate risk): These trials evaluate the effectiveness of the treatment. (12 trials available)
(3) Phase 3 (lower risk): These trials compare the new treatment to the current standard. (8 trials available)
(4) Trials where the phase is listed as N/A. (4 trials available)

Please select the phase you are most comfortable with by choosing the corresponding number.

You: 2

Assistant: (Question 2) Please confirm (y/n): Phase 2 (moderate risk): These trials evaluate the effectiveness of the treatment. (12 trials available)

EXAMPLE 2:

Assistant: (Question 1) How long are you willing to commit to a clinical trial? There are 20 trials available based on your answer.

(1) Approximately 6 months to 1 year (8 trials available)
(2) Approximately 1 year 1 month to 3 years (7 trials available)
(3) Approximately 3 years 1 month to 6 years (5 trials available)

Please choose the option that best suits your availability by selecting the corresponding number.

You: 3

Assistant: (Question 1) Please confirm (y/n): Approximately 3 years 1 month to 6 years (5 trials available)

Assistant: (Question 2) Which phase of clinical trials are you comfortable participating in? There are 26 trials available based on your answer.

(1) Phase 1 (highest risk): These trials focus on assessing the safety of a new treatment. (10 trials available)
(2) Phase 2 (moderate risk): These trials evaluate the effectiveness of the treatment. (9 trials available)
(3) Phase 3 (lower risk): These trials compare the new treatment to the current standard. (5 trials available)
(4) Trials where the phase is listed as N/A. (2 trials available)

Please select the phase you are most comfortable with by choosing the corresponding number.

You: 4

Assistant: (Question 2) Please confirm (y/n): Trials where the phase is listed as N/A. (2 trials available)

EXAMPLE 3:

Assistant: (Question 1) How long are you willing to commit to a clinical trial? There are 12 trials available based on your answer.

(1) Approximately 3 months to 9 months (4 trials available)
(2) Approximately 10 months to 2 years (5 trials available)
(3) Approximately 2 years 1 month to 4 years (3 trials available)

Please choose the option that best suits your availability by selecting the corresponding number.

You: 2

Assistant: (Question 1) Please confirm (y/n): Approximately 10 months to 2 years (5 trials available)

Assistant: (Question 2) Which phase of clinical trials are you comfortable participating in? There are 12 trials available based on your answer.

(1) Phase 1 (highest risk): These trials focus on assessing the safety of a new treatment. (5 trials available)
(2) Phase 2 (moderate risk): These trials evaluate the effectiveness of the treatment. (4 trials available)
(3) Phase 3 (lower risk): These trials compare the new treatment to the current standard. (3 trials available)

Please select the phase you are most comfortable with by choosing the corresponding number.

You: 3

Assistant: (Question 2) Please confirm (y/n): Phase 3 (lower risk): These trials compare the new treatment to the current standard. (3 trials available)

EXAMPLE 4:

Assistant: (Question 1) How long are you willing to commit to a clinical trial? There are 18 trials available based on your answer.

(1) Approximately 6 months to 1 year (8 trials available)
(2) Approximately 1 year to 3 years (10 trials available)

Please choose the option that best suits your availability by selecting the corresponding number.

You: 2

Assistant: (Question 1) Please confirm (y/n): Approximately 1 year to 3 years (10 trials available)

Assistant: (Question 2) Which phase of clinical trials are you comfortable participating in? There are 21 trials available based on your answer.

(1) Phase 1 (highest risk): These trials focus on assessing the safety of a new treatment. (5 trials available)
(2) Phase 2 (moderate risk): These trials evaluate the effectiveness of the treatment. (6 trials available)
(3) Phase 3 (lower risk): These trials compare the new treatment to the current standard. (4 trials available)
(4) Phase 4 (post-marketing surveillance): These trials monitor long-term effects and effectiveness after the treatment is on the market. (3 trials available)
(5) Trials where the phase is listed as N/A. (3 trials available)

Please select the phase you are most comfortable with by choosing the corresponding number.

You: 3

Assistant: (Question 2) Please confirm (y/n): Phase 3 (lower risk): These trials compare the new treatment to the current standard. (4 trials available)

EXAMPLE 5:

Assistant: (Question 1) How long are you willing to commit to a clinical trial? There are 60 trials available based on your answer.

(1) Less than 6 months (10 trials available)
(2) 6 months to 1 year (12 trials available)
(3) 1 year to 2 years (14 trials available)
(4) 2 years to 3 years (12 trials available)
(5) More than 3 years (12 trials available)

Please choose the option that best suits your availability by selecting the corresponding number.

You: 3

Assistant: (Question 1) Please confirm (y/n): 1 year to 2 years (14 trials available)

Assistant: (Question 2) Which phase of clinical trials are you comfortable participating in? There are 68 trials available based on your answer.

(1) Phase 1 (highest risk): These trials focus on assessing the safety of a new treatment. (15 trials available)
(2) Phase 2 (moderate risk): These trials evaluate the effectiveness of the treatment. (18 trials available)
(3) Phase 3 (lower risk): These trials compare the new treatment to the current standard. (14 trials available)
(4) Phase 4 (post-marketing surveillance): These trials monitor long-term effects and effectiveness after the treatment is on the market. (11 trials available)
(5) Trials where the phase is listed as N/A. (10 trials available)

Please select the phase you are most comfortable with by choosing the corresponding number.

You: 2

Assistant: (Question 2) Please confirm (y/n): Phase 2 (moderate risk): These trials evaluate the effectiveness of the treatment. (18 trials available)
"""}

initial_message = """Found 43 Trials for Triple-Negative Breast Cancer within 203 Miles of New York, NY—Let’s Narrow the Results with a few questions."""
