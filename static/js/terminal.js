const socket = io();
const container = document.getElementById('terminal-container');
const themeToggle = document.getElementById('theme-toggle');
const newTerminalButton = document.getElementById('new-terminal');
let inputLine = null;

// Function to handle command input
function createInputLine() {
    inputLine = document.createElement('div');
    inputLine.innerHTML = '$ <span contenteditable="true" class="input-span" spellcheck="false"></span>';
    container.appendChild(inputLine);
    
    const inputSpan = inputLine.querySelector('.input-span');
    inputSpan.focus();
    
    // Listen for 'Enter' key
    inputSpan.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault(); // Prevents new line
            const command = inputSpan.textContent;
            socket.emit('terminal_input', { input: command + '\r' });
            inputSpan.contentEditable = false;
            createInputLine();
        }
    });
    
    // Scroll to the bottom
    container.scrollTop = container.scrollHeight;
}

// Handle incoming output from the server
socket.on('terminal_output', function(data) {
    // Create an instance of AnsiUp
    const ansi_up = new AnsiUp();

    // Convert ANSI codes to HTML
    const htmlOutput = ansi_up.ansi_to_html(data.output);

    // Remove the current input line to add output
    if (inputLine) {
        container.removeChild(inputLine);
    }

    // Create a new div for the output and set the HTML
    const outputLine = document.createElement('div');
    outputLine.classList.add('terminal-line');
    outputLine.innerHTML = htmlOutput; // Use innerHTML to render HTML
    container.appendChild(outputLine);

    // Recreate the input line
    createInputLine();
});

// Create a new terminal session
newTerminalButton.addEventListener('click', function() {
    socket.emit('create_terminal');
});

socket.on('terminal_created', function() {
    container.innerHTML = '';
    createInputLine();
});

// Initial call to create the input line
createInputLine();