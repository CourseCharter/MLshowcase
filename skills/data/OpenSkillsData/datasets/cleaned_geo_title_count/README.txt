
            Counts of job posting title occurrences by CBSA.

            Includes:
- The top ONET skills (KSATs) extracted from the job postings
    of the given job title
- The top predicted ONET SOC codes from two different in-development
    versions of our classifier based on job posting content
    of the given job title
- The top ONET SOC codes given to us by the data partner
    for job postings of the given job title


            Job titles are cleaned by lowercasing, removing punctuation, and removing city and state names.
Each file contains the data for job postings active in one quarter.
If a job posting was active in two quarters,
it will be present in the counts of both quarters.