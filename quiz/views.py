from django.shortcuts import render, get_object_or_404, redirect
from .models import Quiz

def quiz_list(request):
    quizzes = Quiz.objects.all()
    return render(request, 'quiz/quiz_list.html', {'quizzes': quizzes})

def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    if request.method == "POST":
        questions = quiz.questions.all()
        score = 0
        total = questions.count()

        for question in questions:
            selected_option = request.POST.get(str(question.id))
            if selected_option:
                correct_option = question.answers.filter(is_correct=True).first()
                if str(correct_option.id) == selected_option:
                    score += 1

        percentage = round((score / total) * 100, 2)
        return render(request, 'quiz/result.html', {'quiz': quiz, 'score': score, 'total': total, 'percentage': percentage})

    return render(request, 'quiz/take_quiz.html', {'quiz': quiz})

from .forms import QuizForm, QuestionForm, AnswerForm
from .models import Question, Answer

def create_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            return redirect('create_question', quiz_id=quiz.id)  # Redirect to question creation page
    else:
        form = QuizForm()

    return render(request, 'quiz/create_quiz.html', {'form': form})

def create_question(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz  # Associate the question with the selected quiz
            question.save()
            return redirect('create_answer', question_id=question.id)  # Redirect to answer creation page
    else:
        form = QuestionForm(initial={'quiz': quiz})

    return render(request, 'quiz/create_question.html', {'form': form, 'quiz': quiz})

def create_answer(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            form.save()  # Save the answer
            return redirect('create_question', quiz_id=question.quiz.id)  # Go back to question creation page
    else:
        form = AnswerForm(initial={'question': question})

    return render(request, 'quiz/create_answer.html', {'form': form, 'question': question})
