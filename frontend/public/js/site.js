const faqAnswers = [
    {
        terms: ['services', 'what do you do', 'provide'],
        answer: 'AI Hub helps with AI consulting, workflow automation, custom chatbots, data intelligence, and practical AI training.'
    },
    {
        terms: ['chatbot', 'chatbots', 'virtual assistant'],
        answer: 'Yes. AI Hub builds website chatbots, support assistants, internal knowledge assistants, and FAQ automation.'
    },
    {
        terms: ['price', 'pricing', 'cost'],
        answer: 'Pricing depends on the project scope, timeline, data, and integrations. Share your requirements for a proper estimate.'
    },
    {
        terms: ['training', 'workshop', 'team'],
        answer: 'Yes. AI Hub offers practical AI training, workshops, adoption roadmaps, and responsible AI guidance for teams.'
    },
    {
        terms: ['contact', 'email', 'phone'],
        answer: 'You can contact AI Hub at aihub@gmail.com or call +977 98011101011.'
    },
    {
        terms: ['hours', 'open', 'time'],
        answer: 'AI Hub is available Monday to Friday, 9:00 AM - 5:00 PM.'
    }
];

function getAssistantAnswer(question) {
    const normalized = question.toLowerCase();
    const match = faqAnswers.find((faq) => faq.terms.some((term) => normalized.includes(term)));
    return match ? match.answer : 'Please contact AI Hub at aihub@gmail.com with your requirement so the team can guide you.';
}

function setupChat(formId, feedId, inputId, quickSelector) {
    const form = document.getElementById(formId);
    const feed = document.getElementById(feedId);
    const input = document.getElementById(inputId);
    const quickQuestions = document.querySelectorAll(quickSelector);

    if (!form || !feed || !input) {
        return;
    }

    const addMessage = (text, type) => {
        const message = document.createElement('div');
        message.className = `message ${type}`;
        message.textContent = text;
        feed.appendChild(message);
        feed.scrollTop = feed.scrollHeight;
    };

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        const question = input.value.trim();
        if (!question) {
            return;
        }

        addMessage(question, 'user');
        input.value = '';
        window.setTimeout(() => addMessage(getAssistantAnswer(question), 'assistant'), 250);
    });

    quickQuestions.forEach((button) => {
        button.addEventListener('click', () => {
            input.value = button.dataset.question || button.textContent.trim();
            form.requestSubmit();
        });
    });
}

function setupWidget() {
    const widget = document.querySelector('.assistant-widget');
    if (!widget) {
        return;
    }

    const toggle = widget.querySelector('.assistant-widget-toggle');
    const panel = widget.querySelector('.assistant-widget-panel');
    const closeButton = widget.querySelector('.assistant-widget-header button');

    const setOpen = (isOpen) => {
        panel.hidden = !isOpen;
        toggle.setAttribute('aria-expanded', String(isOpen));
        if (isOpen) {
            const input = widget.querySelector('#assistant-widget-question');
            input && input.focus();
        }
    };

    toggle.addEventListener('click', () => setOpen(panel.hidden));
    closeButton.addEventListener('click', () => setOpen(false));
}

function setupStaticContactForm() {
    const form = document.getElementById('contact-form');
    const message = document.getElementById('contact-form-message');
    if (!form || !message) {
        return;
    }

    form.addEventListener('submit', (event) => {
        event.preventDefault();
        message.hidden = false;
        message.textContent = 'Frontend-only demo: please send your request to aihub@gmail.com or call +977 98011101011.';
        form.reset();
    });
}

document.addEventListener('DOMContentLoaded', () => {
    setupWidget();
    setupChat('assistant-widget-form', 'assistant-widget-feed', 'assistant-widget-question', '.assistant-widget-questions button');
    setupChat('assistant-form', 'chat-feed', 'assistant-question', '.quick-questions button');
    setupStaticContactForm();
});

