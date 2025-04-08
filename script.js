class Notepad {
    constructor() {
        this.editor = document.querySelector('.editor');
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.adaptLayout();
        this.setupFullscreen();
        this.checkMobile();
    }

    setupEventListeners() {
        document.querySelectorAll('.btn').forEach(btn => {
            btn.addEventListener('click', () => this.handleAction(btn.dataset.action));
        });

        document.querySelector('.font-size').addEventListener('change', (e) => {
            this.formatText('fontSize', e.target.value + 'px');
        });

        document.querySelector('.color-picker').addEventListener('input', (e) => {
            this.formatText('foreColor', e.target.value);
        });

        window.addEventListener('resize', () => this.adaptLayout());
    }

    handleAction(action) {
        const actions = {
            bold: () => this.formatText('bold'),
            italic: () => this.formatText('italic'),
            copy: () => this.copyText(),
            paste: () => this.pasteText(),
            print: () => this.printContent(),
            save: () => this.saveFile(),
            fullscreen: () => this.toggleFullscreen()
        };
        
        if (actions[action]) actions[action]();
    }

    formatText(command, value = null) {
        document.execCommand(command, false, value);
        this.editor.focus();
    }

    async copyText() {
        try {
            await navigator.clipboard.writeText(window.getSelection().toString());
            this.showToast('Text copied! 📋');
        } catch (err) {
            console.error('Copy failed:', err);
        }
    }

    async pasteText() {
        try {
            const text = await navigator.clipboard.readText();
            document.execCommand('insertText', false, text);
            this.showToast('Text pasted! 📎');
        } catch (err) {
            console.error('Paste failed:', err);
        }
    }

    printContent() {
        const content = this.editor.innerHTML;
        const printWindow = window.open('', '_blank');
        printWindow.document.write(`
            <html>
                <head><title>Print Document</title></head>
                <body style="padding: 20px; font-family: Arial;">${content}</body>
            </html>
        `);
        printWindow.document.close();
        printWindow.print();
    }

    saveFile() {
        const text = this.editor.innerText;
        const blob = new Blob([text], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `note_${new Date().toISOString().slice(0,10)}.txt`;
        a.click();
        URL.revokeObjectURL(url);
        this.showToast('File saved! 💾');
    }

    adaptLayout() {
        const isVertical = window.innerWidth < window.innerHeight;
        if (isVertical) {
            document.body.classList.add('mobile-layout');
        } else {
            document.body.classList.remove('mobile-layout');
        }
    }

    setupFullscreen() {
        document.addEventListener('fullscreenchange', () => {
            const btn = document.querySelector('.fullscreen-btn i');
            btn.classList.toggle('fa-expand');
            btn.classList.toggle('fa-compress');
        });
    }

    toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            document.exitFullscreen();
        }
    }

    checkMobile() {
        if ('ontouchstart' in window) {
            this.editor.addEventListener('focus', () => {
                document.querySelector('.mobile-keyboard-hint').style.display = 'none';
            });
        }
    }

    showToast(message) {
        const toast = document.createElement('div');
        toast.className = 'toast-message';
        toast.textContent = message;
        document.body.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 2000);
    }
}

// Initialize app
new Notepad();