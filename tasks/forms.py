from django import forms
from django.contrib.auth.models import User
from .models import Task, Employee

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'priority', 'status', 'assigned_to']


class EmployeeForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Employee
        fields = ['role']

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=self.cleaned_data['password']
        )

        employee = Employee(user=user, role=self.cleaned_data['role'])

        if commit:
            user.save()
            employee.save()

        return employee