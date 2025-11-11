class TaskDeadlineExceedsProjectDeadlineException(Exception):
    
    def __init__(self, task_deadline, project_deadline):
        self.task_deadline = task_deadline
        self.project_deadline = project_deadline
        super().__init__(
            f"Task deadline {task_deadline} exceeds project deadline {project_deadline}"
        )


