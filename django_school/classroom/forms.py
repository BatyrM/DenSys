from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError

from classroom.models import (Answer, Question, Patient, Teacher, PatientAnswer,
                              Subject, User)


class TeacherSignUpForm(UserCreationForm):
    content = forms.CharField(label='Content', max_length=100)
    certificate = forms.CharField(label='Certficate', max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'content', 'iin', 'certificate']
    
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_teacher = True
        user.save()
        teacher = Teacher.objects.create(user=user)
        teacher.certificate = self.cleaned_data.get('certificate')
        teacher.save()
        return user


class PatientSignUpForm(UserCreationForm):
    interests = forms.ModelChoiceField(
        queryset=Subject.objects.all(),
        widget=forms.Select,
        required=True
    )
    content = forms.CharField(label='Content', max_length=100)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'content', 'iin']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_patient = True
        user.save()
        patient = Patient.objects.create(user=user)
        # patient.interests.add(*self.cleaned_data.get('interests'))
        return user


class PatientInterestsForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError('Mark at least one answer as correct.', code='no_correct_answer')


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = PatientAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')
