document.addEventListener("DOMContentLoaded", () => {
    const cells = document.querySelectorAll(".cell");
    const resetButton = document.getElementById("reset-button");
    const modal = document.getElementById("modal");
    const modalMessage = document.getElementById("modal-message");
    const modalGif = document.getElementById("modal-gif");
    const milestoneButton = document.getElementById("milestone-button");
    const milestoneModal = document.getElementById("milestone-modal");
    const closeModal = document.getElementById("close-modal");
    const closeMilestoneModal = document.getElementById("close-milestone-modal");

    // Handle cell clicks
    cells.forEach(cell => {
        cell.addEventListener("click", () => {
            const row = cell.getAttribute("data-row");
            const col = cell.getAttribute("data-col");

            fetch("/move", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ row, col })
            })
                .then(response => response.json())
                .then(data => {
                    if (data.status === "invalid") return;

                    cell.innerHTML = '<img src="/static/images/santa.png" alt="Santa" width="60" height="60">';

                    if (data.ai_move) {
                        const aiCell = document.querySelector(
                            `.cell[data-row="${data.ai_move[0]}"][data-col="${data.ai_move[1]}"]`
                        );
                        aiCell.innerHTML = '<img src="/static/images/grinch.png" alt="Grinch" width="60" height="60">';
                    }

                    if (data.status === "win" || data.status === "draw") {
                        setTimeout(() => {
                            if (data.status === "win") {
                                modalMessage.textContent = data.winner === "Santa" ? "You Win!" : "Try Again!";
                                modalGif.src = data.winner === "Santa" 
                                    ? "/static/images/win.gif" 
                                    : "/static/images/loss.gif";
                                milestoneButton.style.display = data.winner === "Santa" ? "block" : "none";
                            } else {
                                modalMessage.textContent = "It's a draw!";
                                modalGif.src = "/static/images/draw.gif";
                                milestoneButton.style.display = "block";
                            }
                            modal.style.display = "block";
                        }, 500);
                    }
                })
                .catch(error => console.error("Error:", error));
        });
    });

    milestoneButton.addEventListener("click", () => {
        milestoneModal.style.display = "block";
    });

    closeMilestoneModal.addEventListener("click", () => {
        milestoneModal.style.display = "none";
    });

    resetButton.addEventListener("click", () => {
        fetch("/reset", { method: "POST" })
            .then(() => {
                cells.forEach(cell => (cell.innerHTML = ""));
                modal.style.display = "none";
                milestoneModal.style.display = "none";
                modalGif.src = "";
            });
    });

    function resetGame() {
        fetch("/reset", { method: "POST" })
            .then(() => {
                // Clear the board visually
                const cells = document.querySelectorAll(".cell");
                cells.forEach(cell => (cell.innerHTML = ""));
                modal.style.display = "none"; // Close the modal
            })
            .catch(error => console.error("Error resetting the game:", error));
    }

    closeModal.addEventListener("click", () => {
        resetGame(); // Automatically reset the game when the modal is closed
    });
});