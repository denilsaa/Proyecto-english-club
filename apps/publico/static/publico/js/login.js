// Esperar a que se cargue el DOM
document.addEventListener('DOMContentLoaded', function() {
    // Referencias a elementos del DOM
    const roleOptions = document.querySelectorAll(".role-option");
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');
    const eyeIcon = document.getElementById('eyeIcon');
    const eyeOffIcon = document.getElementById('eyeOffIcon');
    const loginForm = document.getElementById('loginForm');
    const usernameInput = document.getElementById('username');
    const submitBtn = document.getElementById('submitBtn');

    // Función para manejar la selección de roles
    roleOptions.forEach(option => {
        option.addEventListener("click", () => {
            // Eliminar clase activa de todos los roles
            roleOptions.forEach(o => {
                o.classList.remove("ring-2", "ring-blue-500", "bg-blue-100", "shadow-md");
                o.querySelector('.role-text').classList.remove("text-blue-800");
                o.querySelector('.role-text').classList.add("text-gray-700");
            });
            
            // Agregar clase activa al rol seleccionado con animación
            option.classList.add("ring-2", "ring-blue-500", "bg-blue-100", "shadow-md");
            option.querySelector('.role-text').classList.remove("text-gray-700");
            option.querySelector('.role-text').classList.add("text-blue-800");
        });
    });

    // Función para mostrar/ocultar contraseña
    if (togglePassword) {
        togglePassword.addEventListener('click', function() {
            // Cambiar el tipo de input
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);
            
            // Cambiar el ícono
            eyeIcon.classList.toggle('hidden');
            eyeOffIcon.classList.toggle('hidden');
            
            // Agregar un pequeño efecto de rotación
            this.style.transition = 'transform 0.3s ease';
            this.style.transform = 'rotate(180deg)';
            setTimeout(() => {
                this.style.transform = 'rotate(0deg)';
            }, 300);
        });
    }

    // Efecto de ripple para botones y áreas clickeables
    function createRipple(event) {
        const button = event.currentTarget;

        const circle = document.createElement('span');
        const diameter = Math.max(button.clientWidth, button.clientHeight);
        const radius = diameter / 2;

        circle.style.width = circle.style.height = `${diameter}px`;
        circle.style.left = `${event.clientX - button.getBoundingClientRect().left - radius}px`;
        circle.style.top = `${event.clientY - button.getBoundingClientRect().top - radius}px`;
        circle.classList.add('ripple');

        const ripple = button.getElementsByClassName('ripple')[0];
        if (ripple) {
            ripple.remove();
        }

        button.appendChild(circle);
    }

    // Aplicar efecto ripple a botones y opciones de rol
    const buttons = document.querySelectorAll('button, .role-option');
    buttons.forEach(button => {
        button.addEventListener('click', createRipple);
    });

    // Validación del formulario
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            let isValid = true;
            let roleSelected = false;
            
            // Verificar que se seleccionó un rol
            roleOptions.forEach(option => {
                const radio = option.querySelector('input[type="radio"]');
                if (radio.checked) {
                    roleSelected = true;
                }
            });
            
            if (!roleSelected) {
                isValid = false;
                showError('Por favor seleccione un tipo de usuario');
                
                // Efecto de shake en el selector de roles
                const roleSelector = document.getElementById('role-selector');
                roleSelector.classList.add('animate__animated', 'animate__shakeX');
                setTimeout(() => {
                    roleSelector.classList.remove('animate__animated', 'animate__shakeX');
                }, 1000);
            }
            
            // Verificar campos obligatorios con animación
            if (usernameInput.value.trim() === '') {
                isValid = false;
                usernameInput.classList.add('ring-2', 'ring-red-500');
                applyShakeEffect(usernameInput.parentElement);
                showError('El campo usuario es obligatorio');
            } else {
                usernameInput.classList.remove('ring-2', 'ring-red-500');
            }
            
            if (passwordInput.value.trim() === '') {
                isValid = false;
                passwordInput.classList.add('ring-2', 'ring-red-500');
                applyShakeEffect(passwordInput.parentElement);
                showError('El campo contraseña es obligatorio');
            } else {
                passwordInput.classList.remove('ring-2', 'ring-red-500');
            }
            
            if (!isValid) {
                event.preventDefault();
            } else {
                // Efecto de carga al enviar el formulario
                submitBtn.innerHTML = 'Procesando...';
                submitBtn.classList.add('opacity-75', 'cursor-wait', 'loading');
            }
        });
    }

    // Función para aplicar efecto shake a elementos
    function applyShakeEffect(element) {
        element.classList.add('animate__animated', 'animate__shakeX');
        setTimeout(() => {
            element.classList.remove('animate__animated', 'animate__shakeX');
        }, 1000);
    }

    // Función para mostrar mensajes de error
    function showError(message) {
        // Verificar si ya existe un mensaje de error
        let existingError = document.querySelector('.error-message');
        if (existingError) {
            // Si ya existe un error, simplemente actualizar el mensaje y reiniciar la animación
            existingError.innerHTML = `<p class="text-sm">${message}</p>`;
            existingError.classList.remove('animate__fadeIn');
            void existingError.offsetWidth; // Trigger reflow para reiniciar la animación
            existingError.classList.add('animate__fadeIn');
        } else {
            // Crear nuevo mensaje de error
            const errorDiv = document.createElement('div');
            errorDiv.className = 'error-message bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded mt-4 animate__animated animate__fadeIn';
            errorDiv.innerHTML = `<p class="text-sm">${message}</p>`;
            
            // Insertar después del formulario
            loginForm.insertAdjacentElement('afterend', errorDiv);
        }
        
        // Eliminar después de 5 segundos
        setTimeout(() => {
            const currentError = document.querySelector('.error-message');
            if (currentError) {
                currentError.classList.add('animate__fadeOut');
                setTimeout(() => {
                    if (currentError.parentNode) {
                        currentError.parentNode.removeChild(currentError);
                    }
                }, 500);
            }
        }, 5000);
    }

    // Agregar efecto de enfoque/desenfoque para inputs
    const inputs = document.querySelectorAll('input[type="text"], input[type="password"]');
    inputs.forEach(input => {
        const parentDiv = input.parentElement;
        
        input.addEventListener('focus', () => {
            parentDiv.classList.add('input-focus');
        });
        
        input.addEventListener('blur', () => {
            parentDiv.classList.remove('input-focus');
        });
    });

    // Detectar y señalar interacciones con el teclado para accesibilidad
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });

    // Añadir la clase 'loaded' al body para activar las animaciones iniciales de entrada
    setTimeout(() => {
        document.body.classList.add('loaded');
    }, 100);
});