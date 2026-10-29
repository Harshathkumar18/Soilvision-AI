/* ============================================================
   SoilVision AI — Educational Quiz Engine
   Beginner & Advanced multiple-choice quizzes, instant scientific
   explanations, progress tracking, and leaderboard submission.
   ============================================================ */
'use strict';

let currentQuestions = [];
let currentQuestionIndex = 0;
let userAnswers = {};
let currentDifficulty = 'beginner';
let selectedOptionIndex = null;

document.addEventListener('DOMContentLoaded', () => {
  initQuizControls();
  loadQuizQuestions('beginner');
});

function initQuizControls() {
  const diffButtons = document.querySelectorAll('.btn-diff-select');
  diffButtons.forEach(btn => {
    btn.addEventListener('click', (e) => {
      diffButtons.forEach(b => {
        b.classList.remove('active', 'btn-primary');
        b.classList.add('btn-ghost');
      });
      e.currentTarget.classList.add('active', 'btn-primary');
      e.currentTarget.classList.remove('btn-ghost');
      currentDifficulty = e.currentTarget.getAttribute('data-difficulty');
      const badge = document.getElementById('quizDiffBadge');
      if (badge) badge.textContent = currentDifficulty.charAt(0).toUpperCase() + currentDifficulty.slice(1);
      loadQuizQuestions(currentDifficulty);
    });
  });

  const nextBtn = document.getElementById('quizNextBtn');
  if (nextBtn) {
    nextBtn.addEventListener('click', handleNextQuestion);
  }

  const restartBtn = document.getElementById('quizRestartBtn');
  if (restartBtn) {
    restartBtn.addEventListener('click', () => {
      loadQuizQuestions(currentDifficulty);
    });
  }
}

async function loadQuizQuestions(difficulty) {
  const card = document.getElementById('quizQuestionCard');
  const resultsView = document.getElementById('quizResultsCard');
  const loading = document.getElementById('quizLoading');

  if (resultsView) resultsView.style.display = 'none';
  if (card) card.style.display = 'none';
  if (loading) loading.style.display = 'flex';

  currentQuestionIndex = 0;
  userAnswers = {};
  selectedOptionIndex = null;

  try {
    const res = await fetch(`/api/quiz-questions?difficulty=${difficulty}`);
    const data = await res.json();
    currentQuestions = data.questions || [];

    if (loading) loading.style.display = 'none';
    if (card) card.style.display = 'block';

    renderCurrentQuestion();
  } catch (err) {
    console.error('Failed to load quiz questions:', err);
    if (loading) {
      loading.innerHTML = '<p class="text-sm" style="color: var(--clr-danger);">Could not load quiz questions. Please check your connection.</p>';
    }
  }
}

function renderCurrentQuestion() {
  if (currentQuestionIndex >= currentQuestions.length) {
    finishQuiz();
    return;
  }

  selectedOptionIndex = null;
  const q = currentQuestions[currentQuestionIndex];
  const progressText = document.getElementById('quizProgressText');
  const progressBar = document.getElementById('quizProgressBar');
  const questionText = document.getElementById('quizQuestionText');
  const optionsContainer = document.getElementById('quizOptionsContainer');
  const feedbackBox = document.getElementById('quizExplanationBox');
  const nextBtn = document.getElementById('quizNextBtn');

  // Progress
  const progressPct = (currentQuestionIndex / currentQuestions.length) * 100;
  if (progressBar) progressBar.style.width = `${progressPct}%`;
  if (progressText) progressText.innerText = `Question ${currentQuestionIndex + 1} of ${currentQuestions.length}`;

  // Question
  if (questionText) questionText.innerText = q.question;

  // Reset feedback and next button
  if (feedbackBox) {
    feedbackBox.classList.remove('visible');
    feedbackBox.style.display = 'none';
  }
  if (nextBtn) {
    nextBtn.disabled = true;
    nextBtn.innerText = (currentQuestionIndex === currentQuestions.length - 1) ? 'Submit Quiz & View Results' : 'Next Question \u2192';
  }

  // Render Options
  const letters = ['A', 'B', 'C', 'D'];
  if (optionsContainer) {
    optionsContainer.innerHTML = q.options.map((opt, idx) => `
      <button type="button" class="quiz-option" id="optBtn_${idx}" onclick="selectQuizOption(${idx})">
        <span class="quiz-option-letter">${letters[idx]}</span>
        <span>${opt}</span>
      </button>
    `).join('');
  }
}

window.selectQuizOption = function(chosenIdx) {
  if (selectedOptionIndex !== null) return; // Prevent changing answer after selection
  selectedOptionIndex = chosenIdx;

  const q = currentQuestions[currentQuestionIndex];
  userAnswers[q.id] = chosenIdx;

  const isCorrect = (chosenIdx === q.answer_index);
  const options = document.querySelectorAll('.quiz-option');

  // Style chosen and correct options
  options.forEach((btn, idx) => {
    btn.disabled = true;
    if (idx === q.answer_index) {
      btn.classList.add('correct');
    } else if (idx === chosenIdx && !isCorrect) {
      btn.classList.add('incorrect');
    }
  });

  // Show explanation
  const feedbackBox = document.getElementById('quizExplanationBox');
  const feedbackText = document.getElementById('quizExplanationText');
  if (feedbackBox && feedbackText) {
    feedbackText.innerHTML = `<strong>${isCorrect ? '✓ Correct! ' : '✗ Incorrect. '}</strong>${q.explanation}`;
    feedbackBox.style.display = 'block';
    feedbackBox.classList.add('visible');
  }

  // Enable next button
  const nextBtn = document.getElementById('quizNextBtn');
  if (nextBtn) nextBtn.disabled = false;
};

function handleNextQuestion() {
  currentQuestionIndex++;
  if (currentQuestionIndex < currentQuestions.length) {
    renderCurrentQuestion();
  } else {
    finishQuiz();
  }
}

async function finishQuiz() {
  const card = document.getElementById('quizQuestionCard');
  const resultsView = document.getElementById('quizResultsCard');
  const loading = document.getElementById('quizLoading');

  if (card) card.style.display = 'none';
  if (loading) loading.style.display = 'flex';

  const nameInput = document.getElementById('quizPlayerName');
  const playerName = (nameInput && nameInput.value.trim()) ? nameInput.value.trim() : 'Soil Friend';

  try {
    const res = await fetch('/api/quiz-submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        difficulty: currentDifficulty,
        player_name: playerName,
        answers: userAnswers
      })
    });
    const result = await res.json();

    if (loading) loading.style.display = 'none';
    if (resultsView) resultsView.style.display = 'block';

    const pctEl = document.getElementById('quizScorePct');
    const titleEl = document.getElementById('quizResultTitle');
    const msgEl = document.getElementById('quizResultMsg');

    if (pctEl) pctEl.innerText = `${Math.round(result.percentage)}%`;

    if (titleEl && msgEl) {
      if (result.percentage >= 80) {
        titleEl.innerText = 'Outstanding Agronomy Mastery! 🏆';
        msgEl.innerText = `You answered ${result.score} out of ${result.total} questions correctly. You have an expert grasp of ICAR soil benchmarks and conservation practices!`;
      } else if (result.percentage >= 60) {
        titleEl.innerText = 'Good Agronomic Foundation! 🌱';
        msgEl.innerText = `You scored ${result.score} out of ${result.total}. Review the educational cards above to strengthen your understanding of micronutrients and soil organic carbon.`;
      } else {
        titleEl.innerText = 'Keep Exploring Soil Science! 🔬';
        msgEl.innerText = `You scored ${result.score} out of ${result.total}. Expand the soil fundamental cards above and test your knowledge again!`;
      }
    }
  } catch (err) {
    console.error('Quiz submission error:', err);
    if (loading) loading.style.display = 'none';
    if (resultsView) resultsView.style.display = 'block';
  }
}
