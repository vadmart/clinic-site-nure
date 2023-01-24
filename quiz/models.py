from django.db import models


# Create your models here.
class InputType(models.Model):
    type_name = models.CharField(max_length=10)

    def __str__(self):
        return self.type_name


class Question(models.Model):
    question_text = models.CharField(max_length=255)
    input_type = models.ForeignKey(InputType, on_delete=models.CASCADE)

    def __str__(self):
        return f"Question: {self.question_text}, input type: {self.input_type}"


class Answer(models.Model):
    answer_text = models.CharField(max_length=100)

    def __str__(self):
        return self.answer_text


class QuestionAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    is_answer_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"Question: {self.question}, answer: {self.answer}"
