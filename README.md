# FiestaPivot - UNSW Software Engineering Major Project #2

## Disclaimer: 
This Repository contains code for the second project of three completed within Software Engineering. This project was completed in 18s2. This was completed as a group assignment, and remains the work of the individuals listed below. You are free to view, use, run and modify this application in any way you like. **Please do not use any of the work contained within this project without explicitly attributing the original authors, otherwise you are plagiarising.** We assume no responsibility for any damage, harm or other effects that arise from using this software.

### Group members:
- Bailey Ivancic
- Estella Arabi
- Jacob Wahib
- Nabil Shaikh
- Harry Tang

## Project brief:
In this Software Engineering workshop, our aim was to create an application that followed the specifications set out in the initial brief we were given. A copy of this requirement document is included inthe repository, named *partywhip_initial_specifications.pdf*.

Essentially, our aim was to make an application that worked the same as airtasker, but instead focused solely on the purpose of catering. This allowed people to both post on catering and bidding jobs, giving both the advertiser and job seeker greater power and flexibility.

In addition to making this application, one of the biggest focuses of this project was **Dafny verification**. Since SENG2011 is a verification course, we needed to ensure that whevever possible, our algorithms and functions were verified for correctness with Dafny, before being translated and being put in our application. The Dafny online compiler/verifier can be found [here.](https://rise4fun.com/dafny)

## Project details:
FiestaPivot is a web-based application that aims to revolutionise the catering industry. Previously, there existed a barrier for the advertiser of the job, since they would have to both find and then negotiate with a willing party to get their event catered for. Additionally, this also created a barrier for parties looking for catering work, since no service existed which was dedicated to finding them work which fit their skill level, availability or other requirements. As such, FiestaPivot aims to bring both of these parties into direct contact, and aid both in finding something they are looking for.

FiestaPivot includes the following features:
- Posting ads to be viewed by all users of the site
  - Able to include certain criteria that must be met for a potential applicant
- Bidding on an ad (Applying to fulfil the catering request)
- Choosing one of the offered bids as the successful party
- Searching ads using a wide variety of criteria
- Full control over ads and bids, including deletion, closing, pending
- Rating system, that lets both bidder and advertiser know how the other party has performed at previous events


We are really proud of the application we have put forward, and think that is satisfies the initial brief very well, while also satisfying our own brief of trying to make the experience for both advertiser and bidder as seamless as possible.

### Tech stack:
The application is built on a HTML-CSS-Bootstrap-Jinja2 front-end, using Python with Flask for the back-end requests. SQL has been used for the database.

---

For more information on the project, please have a look at the report documentation included inside the repo, as well as downloading the source code.


## How to use and run FiestaPivot:
1. Clone the repository.
2. Ensure that the Python version you are using is at least 3.6+. Development was done on Python 3.6.
3. Ensure that Python Flask and Flask Login are installed, and upgraded to the latest version.
4. Run command 'Python3 app.py'. This should start up a Flask server.
5. Use the local address and port specified by Flask to use the application.

**This project has now been completed and closed, as of 27/10/18.**
