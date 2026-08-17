const API_URL = "/api";

const taskList = document.getElementById("taskList");
const taskForm = document.getElementById("taskForm");
const taskInput = document.getElementById("taskInput");


async function loadTasks() {
    const response = await fetch(`${API_URL}/tasks`);
    const tasks = await response.json();

    taskList.innerHTML = "";

    tasks.forEach(task => {
        const li = document.createElement("li");

        const title = document.createElement("span");
        title.textContent = task.title;

        if (task.completed) {
            title.classList.add("completed");
        }

        const actions = document.createElement("div");
        actions.className = "actions";

        const toggleButton = document.createElement("button");
        toggleButton.textContent = "Toggle";

        toggleButton.addEventListener("click", async () => {
            await fetch(`${API_URL}/tasks/${task.id}`, {
                method: "PATCH"
            });

            await loadTasks();
        });

        const deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";

        deleteButton.addEventListener("click", async () => {
            await fetch(`${API_URL}/tasks/${task.id}`, {
                method: "DELETE"
            });

            await loadTasks();
        });

        actions.appendChild(toggleButton);
        actions.appendChild(deleteButton);

        li.appendChild(title);
        li.appendChild(actions);

        taskList.appendChild(li);
    });
}


taskForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const title = taskInput.value.trim();

    if (!title) {
        return;
    }

    await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            title: title
        })
    });

    taskInput.value = "";

    await loadTasks();
});


loadTasks();
