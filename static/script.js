const planForm = document.getElementById('plan-form');
const queryInput = document.getElementById('query-input');
const planContainer = document.getElementById('plan-container');
const loader = document.getElementById('loader');
const submitButton = document.getElementById('submit-button');

planForm.addEventListener('submit', async (e) => {
    e.preventDefault(); // Prevent the form from reloading the page
    
    const userQuery = queryInput.value.trim();
    console.log(userQuery)
    if (!userQuery) {
        alert("Please enter a goal.");
        return;
    }

    loader.style.display = 'block';
    submitButton.disabled = true;
    planContainer.innerHTML = ''; 

    try {

        const response = await fetch('/plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: userQuery })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Something went wrong');
        }

        const planData = await response.json();
        renderPlan(planData);

    } catch (error) {
        planContainer.innerHTML = `<p style="color: red; text-align: center;">Error: ${error.message}</p>`;
    } finally {
        loader.style.display = 'none';
        submitButton.disabled = false;
    }
});

function renderPlan(planData) {
    if (!planData || planData.length === 0) {
        planContainer.innerHTML = "<p>No plan could be generated.</p>";
        return;
    }

    let htmlContent = '';
    
    planData.forEach(phase => {
        htmlContent += `
            <div class="phase-card">
                <div class="phase-header">${phase.phase_name}</div>
                <div class="tasks-grid">
        `;
        
        phase.tasks.forEach(task => {
            const dependenciesText = task.dependencies.length > 0
                ? `Depends on: #${task.dependencies.join(', #')}`
                : 'No dependencies';

            htmlContent += `
                <div class="task-card">
                    <h4>${task.task_name} (ID: ${task.task_id})</h4>
                    <p>${task.description}</p>
                    <div class="task-details">
                        <span>🗓️ Day ${task.start_day} - ${task.end_day}</span>
                        <span>🔗 ${dependenciesText}</span>
                    </div>
                </div>
            `;
        });

        htmlContent += `
                </div>
            </div>
        `;
    });

    planContainer.innerHTML = htmlContent;
}


// function showTypingIndicator() {
//     const chatBox = document.getElementById("chatMessages");
//     const typingDiv = document.createElement("div");
//     typingDiv.className = "typing-indicator";
//     typingDiv.id = "typingIndicator";
//     typingDiv.innerHTML = `
//         <span>Bot is typing</span>
//         <div class="typing-dots">
//             <div></div>
//             <div></div>
//             <div></div>
//         </div>
//     `;
//     chatBox.appendChild(typingDiv);
//     chatBox.scrollTop = chatBox.scrollHeight;
// }

// function removeTypingIndicator() {
//     const typingIndicator = document.getElementById("typingIndicator");
//     if (typingIndicator) {
//         typingIndicator.remove();
//     }
// }
