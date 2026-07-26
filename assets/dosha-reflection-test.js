(() => {
    const form = document.getElementById('dosha-reflection-test');

    if (!form) {
        return;
    }

    const result = document.getElementById('dosha-reflection-result');
    const resultTitle = document.getElementById('dosha-reflection-result-title');
    const resultText = document.getElementById('dosha-reflection-result-text');
    const error = document.getElementById('dosha-reflection-error');
    const expectedAnswers = 6;
    let hasTrackedCompletion = false;
    const patterns = {
        vata: {
            name: 'מאפייני הדושה הבולטים מזכירים בעיקר ואטה',
            description: 'בתשובות בלטו יותר תנועה, שינוי, יובש, קור וחוסר סדירות — איכויות המשויכות במסורת לוואטה.'
        },
        pitta: {
            name: 'מאפייני הדושה הבולטים מזכירים בעיקר פיטה',
            description: 'בתשובות בלטו יותר חום, חדות, עוצמה ורגישות — איכויות המשויכות במסורת לפיטה.'
        },
        kapha: {
            name: 'מאפייני הדושה הבולטים מזכירים בעיקר קאפה',
            description: 'בתשובות בלטו יותר כבדות, איטיות, קרירות ויציבות — איכויות המשויכות במסורת לקאפה.'
        }
    };

    form.addEventListener('submit', (event) => {
        event.preventDefault();

        const answers = [...new FormData(form).values()];

        if (answers.length !== expectedAnswers) {
            error.classList.remove('hidden');
            result.classList.add('hidden');
            return;
        }

        const counts = answers.reduce((totals, answer) => {
            totals[answer] += 1;
            return totals;
        }, { vata: 0, pitta: 0, kapha: 0 });
        const highestScore = Math.max(...Object.values(counts));
        const leadingPatterns = Object.keys(counts).filter((pattern) => counts[pattern] === highestScore);

        error.classList.add('hidden');

        if (leadingPatterns.length === 1) {
            const pattern = patterns[leadingPatterns[0]];
            resultTitle.textContent = pattern.name;
            resultText.textContent = `${pattern.description} זו אינה קביעה ש״זו הדושה שלך״, אלא תמונת מצב מצומצמת של התקופה האחרונה.`;
        } else {
            const names = leadingPatterns.map((pattern) => patterns[pattern].name.replace('מאפייני הדושה הבולטים מזכירים בעיקר ', ''));
            resultTitle.textContent = 'עלה דפוס מעורב';
            resultText.textContent = `התשובות התחלקו בין ${names.join(' ו־')}. דפוסים מעורבים שכיחים, ותוצאה כזאת מזכירה למה לא נכון לצמצם אדם לדושה אחת או להסיק ממנה אבחנה.`;
        }

        result.classList.remove('hidden');
        result.focus();

        if (!hasTrackedCompletion && typeof window.gtag === 'function') {
            window.gtag('event', 'dosha_quiz_complete', {
                event_category: 'engagement',
                cta_location: 'dosha-reflection-test',
                transport_type: 'beacon'
            });
            hasTrackedCompletion = true;
        }
    });

    form.addEventListener('reset', () => {
        error.classList.add('hidden');
        result.classList.add('hidden');
        resultTitle.textContent = '';
        resultText.textContent = '';
    });
})();
