import React, { useState, useEffect } from 'react';
import { HelpCircle, CheckCircle, XCircle } from 'lucide-react';
import './QuizView.css';

const QuizView = ({ lessonId }) => {
  const [quiz, setQuiz] = useState(null);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchQuizData();
  }, [lessonId]);

  const fetchQuizData = async () => {
    try {
      const token = localStorage.getItem('token');
      // Fetch quiz
      const qRes = await fetch(`http://localhost:8000/api/v1/quizzes/lesson/${lessonId}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      if (qRes.ok) {
        const qData = await qRes.json();
        setQuiz(qData);
        
        // Fetch questions
        const qsRes = await fetch(`http://localhost:8000/api/v1/quizzes/${qData.id}/questions/full`, {
          headers: { 'Authorization': `Bearer ${token}` }
        });
        if (qsRes.ok) {
          const qsData = await qsRes.json();
          setQuestions(qsData);
        }
      }
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

  const calculateScore = () => {
    let correctCount = 0;
    questions.forEach(q => {
      const selectedAnsId = answers[q.id];
      const selectedAns = q.answers.find(a => a.id === selectedAnsId);
      if (selectedAns && selectedAns.is_correct) {
        correctCount++;
      }
    });
    
    const finalScore = Math.round((correctCount / questions.length) * 100);
    setScore(finalScore);
    setSubmitted(true);
  };

  if (loading) return <div className="p-4 text-center">Test yuklanmoqda...</div>;
  if (!quiz) return <div className="card text-center p-8"><HelpCircle size={48} className="icon-muted mx-auto mb-4"/><h3>Bu darsga test biriktirilmagan</h3></div>;

  return (
    <div className="quiz-container">
      <div className="quiz-header card">
        <h2>{quiz.title}</h2>
        <p className="text-muted">O'tish balli: {quiz.passing_score}%</p>
      </div>

      {submitted && (
        <div className={`quiz-result card ${score >= quiz.passing_score ? 'passed' : 'failed'}`}>
          {score >= quiz.passing_score ? <CheckCircle size={48} /> : <XCircle size={48} />}
          <h2>Natija: {score}%</h2>
          <p>{score >= quiz.passing_score ? "Tabriklaymiz, testdan o'tdingiz!" : "Afsuski, yetarli ball to'play olmadingiz."}</p>
        </div>
      )}

      <div className="questions-list">
        {questions.map((q, idx) => (
          <div key={q.id} className="question-card card">
            <h4 className="question-text">{idx + 1}. {q.text}</h4>
            <div className="answers-list">
              {q.answers.map(ans => {
                const isSelected = answers[q.id] === ans.id;
                let answerClass = "answer-item";
                
                if (submitted) {
                  if (ans.is_correct) answerClass += " correct";
                  else if (isSelected && !ans.is_correct) answerClass += " incorrect";
                } else if (isSelected) {
                  answerClass += " selected";
                }

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
            onClick={calculateScore}
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
