# Submissions

Model used to implement Submissions.

## BaseSubmission

Abstract class that contains the bare minimum for implementation of Submission. Inherits from GeneralFKModel and TimeStamped Model.

  - `user`: *integer*, is the unique identifier for a User. **Required** on object initialization.
  - `submission_time`: *Date and Time*, is the date and time a task was submitted. **Required** on object initialization.
  - `valid`: *boolean*, represents whether a submission is valid or not. It Defaults to False on Initialization of an Object.
  - `status`: *string*, is the status of a submission. It can be either APPROVED, REJECTED, UNDER REVIEW or PENDING REVIEW. It Defaults to PENDING REVIEW on Initialization of an Object.
  - `comments`: *string*.

## Submission

Class that inherits from BaseSubmission and adds linking between a Task and Submission as well as Location and Submission.

  - `task`: *integer*, is a foreign key that links a Task object to a submission. **Required** on object initialization.
  - `location`: *integer*, is a foreign key that links a Location object to a submission. **Required** on object initialization.
