# Submissions

Model representing a submission. A submission is a ...

## BaseSubmission

Abstract class implementing submissions.

_This class inherits from the `GenericFKModel` as such it is able to link to a specific `target` of which we assume is going to be the submission data._

Inherits:
```
tasking.models.base.GenericFKModel
tasking.models.base.TimeStampedModel
django.db.models.Model
```

---

  * user `ForeignKey` - _required_ The user who has submitted the submission.
  * submission_time `DateTimeField` - _required_ The date and time the submission was made.
  * valid `BooleanField`: _Defaults to False_. The validity of the submission.
  * status `CharField`: The status of a submission. It can be either APPROVED, REJECTED, UNDER REVIEW or PENDING REVIEW. It Defaults to PENDING REVIEW on Initialization of an Object.
  * comments `TextField`: The comments given by the reviewer or the requester to the user who created the submission.

## Submission

Concrete class implementing submissions. This implementation of submissions is more focused on recording and tracking location sensitive submissions for a task.

Inherits:
```
BaseSubmission
```

---

  * task `ForeignKey`: _required_ The task of which the submission is being submitted to.
  * location `ForeignKey`: The location the submission was made in.

### Methods

- `get_approved(status)`: Determines whether the status falls under the approved statuses.

### Properties

- approved `Boolean`: Whether the submission has been approved or not.
