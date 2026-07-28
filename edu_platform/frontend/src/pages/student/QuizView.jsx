import React, { useState, useEffect } from 'react';
import { HelpCircle, CheckCircle, XCircle } from 'lucide-react';
import { api } from '../../api';
import './QuizView.css';

const QuizView = ({ lessonId }) => {
  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuizData();
  }, [lessonId]);

  const fetchQuizData = async () => {
    try {
      // Test ma'lumotlari
      const qData = await api(`/quizzes/lesson/${lessonId}`);
      setQuiz(qData);

      // Savollar (is_correct serverda yashiringan)
      const qsData = await api(`/quizzes/${qData.id}/take`);
      setQuestions(qsData);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectAnswer = (questionId, answerId) => {
    if (submitted) return;
    setAnswers({
      ...answers,
      [questionId]: answerId
    });
  };

  const handleSubmit = async () => {
    setError('');
    try {
      // Baholash serverda bajariladi va natija saqlanadi
      const res = await api(`/quizzes/${quiz.id}/submit`, { method: 'POST', body: { answers } });
      setResult(res);
      setSubmitted(true);
    } catch (err) {
      setError("Natijani saqlashda xatolik yuz berdi. Qayta urinib ko'ring.");
    }
  };

  if (loading) return <div className="p-4 text-center">Test yuklanmoqda...</div>;
  if (!quiz) return <div className="card text-center p-8"><HelpCircle size={48} className="icon-muted mx-auto mb-4"/><h3>Bu darsga test biriktirilmagan</h3></div>;

  return (
    <div className="quiz-container">
      <div className="quiz-header card">
        <h2>{quiz.title}</h2>
        <p className="text-muted">O'tish balli: {quiz.passing_score}%</p>
      </div>

      {submitted && result && (
        <div className={`quiz-result card ${result.percent >= quiz.passing_score ? 'passed' : 'failed'}`}>
          {result.percent >= quiz.passing_score ? <CheckCircle size={48} /> : <XCircle size={48} />}
          <h2>Natija: {result.percent}%</h2>
          <p>{result.score}/{result.total} to'g'ri — {result.percent >= quiz.passing_score ? "Tabriklaymiz, testdan o'tdingiz!" : "Afsuski, yetarli ball to'play olmadingiz."}</p>
        </div>
      )}

      {error && <div className="card text-danger p-4">{error}</div>}

      <div className="questions-list">
        {questions.map((q, idx) => (
          <div key={q.id} className="question-card card">
            <h4 className="question-text">{idx + 1}. {q.text}</h4>
            <div className="answers-list">
              {q.answers.map(ans => {
                const isSelected = answers[q.id] === ans.id;
                let answerClass = "answer-item";
                if (isSelected) answerClass += " selected";

                return (
                  <div
                    key={ans.id}
                    className={answerClass}
                    onClick={() => handleSelectAnswer(q.id, ans.id)}
                  >
                    <div className="radio-circle">
                      {isSelected && <div className="radio-dot"></div>}
                    </div>
                    <span>{ans.text}</span>
                  </div>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      {!submitted && questions.length > 0 && (
        <div className="quiz-footer">
          <button
            className="btn-primary full-width"
            onClick={handleSubmit}
            disabled={Object.keys(answers).length < questions.length}
          >
            Natijani bilish
          </button>
        </div>
      )}
    </div>
  );
};

export default QuizView;
