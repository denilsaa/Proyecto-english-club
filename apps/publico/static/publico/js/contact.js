// Variables globales
const form = document.getElementById('contactForm');
const submitBtn = document.getElementById('submitBtn');
const successMessage = document.getElementById('successMessage');
const charCount = document.getElementById('charCount');
const messageTextarea = document.getElementById('message');

// Configuración
const CONFIG = {
  maxMessageLength: 500,
  emailRegex: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  nameMinLength: 2,
  messageMinLength: 10
};

// Estado del formulario
let formState = {
  isValid: false,
  isSubmitting: false,
  fields: {
    name: { isValid: false, value: '' },
    email: { isValid: false, value: '' },
    subject: { isValid: false, value: '' },
    message: { isValid: false, value: '' }
  }
};

// Inicialización cuando el DOM está listo
document.addEventListener('DOMContentLoaded', function() {
  initializeForm();
  addEventListeners();
  addAnimationObserver();
  
  // Mostrar mensaje de bienvenida (opcional)
  console.log('🚀 Formulario de contacto cargado exitosamente');
});

// Función de inicialización
function initializeForm() {
  // Restaurar datos del formulario si existen en localStorage
  const savedData = localStorage.getItem('contactFormData');
  if (savedData) {
    const parsedData = JSON.parse(savedData);
    Object.keys(parsedData).forEach(key => {
      const input = document.getElementById(key);
      if (input) {
        input.value = parsedData[key];
        formState.fields[key] = { isValid: true, value: parsedData[key] };
      }
    });
  }
  
  // Inicializar contador de caracteres
  updateCharacterCount();
}

// Agregar todos los event listeners
function addEventListeners() {
  // Event listeners para validación en tiempo real
  document.getElementById('name').addEventListener('input', debounce(validateName, 300));
  document.getElementById('email').addEventListener('input', debounce(validateEmail, 300));
  document.getElementById('subject').addEventListener('change', validateSubject);
  messageTextarea.addEventListener('input', function() {
    validateMessage();
    updateCharacterCount();
  });
  
  // Guardar datos del formulario en localStorage
  form.addEventListener('input', debounce(saveFormData, 500));
  
  // Envío del formulario
  form.addEventListener('submit', handleFormSubmit);
  
  // Validar al salir del campo (blur)
  ['name', 'email', 'subject', 'message'].forEach(fieldName => {
    document.getElementById(fieldName).addEventListener('blur', function() {
      switch(fieldName) {
        case 'name': validateName(); break;
        case 'email': validateEmail(); break;
        case 'subject': validateSubject(); break;
        case 'message': validateMessage(); break;
      }
    });
  });
  
  // Limpiar errores al hacer focus
  ['name', 'email', 'subject', 'message'].forEach(fieldName => {
    document.getElementById(fieldName).addEventListener('focus', function() {
      clearFieldError(fieldName);
    });
  });
}

// Debounce function para optimizar performance
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Funciones de validación
function validateName() {
  const nameInput = document.getElementById('name');
  const name = nameInput.value.trim();
  const isValid = name.length >= CONFIG.nameMinLength && /^[a-zA-ZÀ-ÿ\s]+$/.test(name);
  
  formState.fields.name = { isValid, value: name };
  
  if (!isValid && name.length > 0) {
    showFieldError('name', 'El nombre debe tener al menos 2 caracteres y solo contener letras');
  } else {
    clearFieldError('name');
    if (isValid) showFieldSuccess('name');
  }
  
  updateFormValidation();
  return isValid;
}

function validateEmail() {
  const emailInput = document.getElementById('email');
  const email = emailInput.value.trim();
  const isValid = CONFIG.emailRegex.test(email);
  
  formState.fields.email = { isValid, value: email };
  
  if (!isValid && email.length > 0) {
    showFieldError('email', 'Por favor, introduce un email válido');
  } else {
    clearFieldError('email');
    if (isValid) showFieldSuccess('email');
  }
  
  updateFormValidation();
  return isValid;
}

function validateSubject() {
  const subjectInput = document.getElementById('subject');
  const subject = subjectInput.value;
  const isValid = subject !== '';
  
  formState.fields.subject = { isValid, value: subject };
  
  if (!isValid) {
    showFieldError('subject', 'Por favor, selecciona un asunto');
  } else {
    clearFieldError('subject');
    showFieldSuccess('subject');
  }
  
  updateFormValidation();
  return isValid;
}

function validateMessage() {
  const message = messageTextarea.value.trim();
  const isValid = message.length >= CONFIG.messageMinLength && message.length <= CONFIG.maxMessageLength;
  
  formState.fields.message = { isValid, value: message };
  
  if (message.length > 0 && message.length < CONFIG.messageMinLength) {
    showFieldError('message', `El mensaje debe tener al menos ${CONFIG.messageMinLength} caracteres`);
  } else if (message.length > CONFIG.maxMessageLength) {
    showFieldError('message', `El mensaje no puede exceder ${CONFIG.maxMessageLength} caracteres`);
  } else {
    clearFieldError('message');
    if (isValid) showFieldSuccess('message');
  }
  
  updateFormValidation();
  return isValid;
}

// Funciones para mostrar errores y éxitos
function showFieldError(fieldName, message) {
  const formGroup = document.getElementById(fieldName).closest('.form-group');
  const errorElement = formGroup.querySelector('.error-message');
  
  formGroup.classList.add('error');
  formGroup.classList.remove('success');
  errorElement.textContent = message;
  
  // Añadir animación
  errorElement.style.animation = 'fadeIn 0.3s ease-out';
}

function clearFieldError(fieldName) {
  const formGroup = document.getElementById(fieldName).closest('.form-group');
  const errorElement = formGroup.querySelector('.error-message');
  
  formGroup.classList.remove('error');
  errorElement.textContent = '';
}

function showFieldSuccess(fieldName) {
  const formGroup = document.getElementById(fieldName).closest('.form-group');
  formGroup.classList.add('success');
  formGroup.classList.remove('error');
}

// Actualizar contador de caracteres
function updateCharacterCount() {
  const currentLength = messageTextarea.value.length;
  charCount.textContent = currentLength;
  
  const characterCountElement = document.querySelector('.character-count');
  characterCountElement.classList.remove('warning', 'danger');
  
  if (currentLength > CONFIG.maxMessageLength * 0.8) {
    characterCountElement.classList.add('warning');
  }
  if (currentLength > CONFIG.maxMessageLength * 0.95) {
    characterCountElement.classList.add('danger');
  }
}

// Actualizar estado global de validación del formulario
function updateFormValidation() {
  const allFieldsValid = Object.values(formState.fields).every(field => field.isValid);
  formState.isValid = allFieldsValid;
  
  // Actualizar estado del botón
  submitBtn.disabled = !allFieldsValid || formState.isSubmitting;
  
  // Cambiar el estilo del botón basado en la validación
  if (allFieldsValid) {
    submitBtn.classList.add('hover:bg-blue-700');
    submitBtn.classList.remove('bg-gray-400');
  } else {
    submitBtn.classList.remove('hover:bg-blue-700');
    submitBtn.classList.add('bg-gray-400');
  }
}

// Manejar envío del formulario
async function handleFormSubmit(event) {
  event.preventDefault();
  
  // Validar todo el formulario una vez más
  const isFormValid = validateName() && validateEmail() && validateSubject() && validateMessage();
  
  if (!isFormValid) {
    showTemporaryMessage('Por favor, corrige los errores antes de enviar', 'error');
    return;
  }
  
  // Cambiar estado a "enviando"
  formState.isSubmitting = true;
  updateButtonState('loading');
  
  try {
    // Simular envío de formulario (aquí irías tu lógica de envío)
    await simulateFormSubmission();
    
    // Éxito
    formState.isSubmitting = false;
    showSuccessMessage();
    resetForm();
    updateButtonState('success');
    
    // Limpiar localStorage
    localStorage.removeItem('contactFormData');
    
  } catch (error) {
    // Error
    formState.isSubmitting = false;
    showTemporaryMessage('Hubo un error al enviar el mensaje. Por favor, intenta de nuevo.', 'error');
    updateButtonState('error');
    console.error('Error al enviar formulario:', error);
  }
}

// Simular envío de formulario
function simulateFormSubmission() {
  return new Promise((resolve, reject) => {
    // Simular tiempo de envío
    setTimeout(() => {
      // 90% de éxito, 10% de error para testing
      if (Math.random() > 0.1) {
        resolve();
      } else {
        reject(new Error('Error simulado'));
      }
    }, 2000);
  });
}

// Actualizar estado visual del botón
function updateButtonState(state) {
  const btnText = submitBtn.querySelector('.btn-text');
  const loadingSpinner = submitBtn.querySelector('.loading-spinner');
  
  switch(state) {
    case 'loading':
      btnText.style.display = 'none';
      loadingSpinner.classList.remove('hidden');
      submitBtn.disabled = true;
      break;
    case 'success':
      btnText.textContent = '¡Enviado!';
      loadingSpinner.classList.add('hidden');
      btnText.style.display = 'inline';
      submitBtn.classList.add('bg-green-600');
      submitBtn.classList.remove('bg-blue-800');
      setTimeout(() => {
        btnText.textContent = 'Enviar mensaje';
        submitBtn.classList.remove('bg-green-600');
        submitBtn.classList.add('bg-blue-800');
        submitBtn.disabled = false;
      }, 3000);
      break;
    case 'error':
      btnText.textContent = 'Error al enviar';
      loadingSpinner.classList.add('hidden');
      btnText.style.display = 'inline';
      submitBtn.classList.add('bg-red-600');
      submitBtn.classList.remove('bg-blue-800');
      setTimeout(() => {
        btnText.textContent = 'Enviar mensaje';
        submitBtn.classList.remove('bg-red-600');
        submitBtn.classList.add('bg-blue-800');
        submitBtn.disabled = false;
      }, 3000);
      break;
    default:
      btnText.style.display = 'inline';
      loadingSpinner.classList.add('hidden');
      submitBtn.disabled = false;
  }
}

// Mostrar mensaje de éxito
function showSuccessMessage() {
  successMessage.classList.remove('hidden');
  successMessage.classList.add('success-animation');
  
  // Scroll al mensaje
  successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });
  
  // Ocultar después de 5 segundos
  setTimeout(() => {
    successMessage.classList.add('hidden');
    successMessage.classList.remove('success-animation');
  }, 5000);
}

// Mostrar mensaje temporal
function showTemporaryMessage(message, type = 'info') {
  const messageContainer = document.createElement('div');
  messageContainer.className = `fixed top-4 right-4 p-4 rounded-lg text-white z-50 transition-all duration-300 transform translate-x-full`;
  
  switch(type) {
    case 'error':
      messageContainer.classList.add('bg-red-500');
      break;
    case 'success':
      messageContainer.classList.add('bg-green-500');
      break;
    default:
      messageContainer.classList.add('bg-blue-500');
  }
  
  messageContainer.textContent = message;
  document.body.appendChild(messageContainer);
  
  // Animar entrada
  setTimeout(() => {
    messageContainer.classList.remove('translate-x-full');
    messageContainer.classList.add('translate-x-0');
  }, 100);
  
  // Animar salida y remover
  setTimeout(() => {
    messageContainer.classList.add('translate-x-full');
    setTimeout(() => {
      if (messageContainer.parentNode) {
        messageContainer.parentNode.removeChild(messageContainer);
      }
    }, 300);
  }, 3000);
}

// Resetear formulario
function resetForm() {
  form.reset();
  
  // Resetear estado
  Object.keys(formState.fields).forEach(key => {
    formState.fields[key] = { isValid: false, value: '' };
    clearFieldError(key);
  });
  
  formState.isValid = false;
  updateFormValidation();
  updateCharacterCount();
}

// Guardar datos del formulario en localStorage
function saveFormData() {
  const formData = {};
  
  ['name', 'email', 'subject', 'message'].forEach(fieldName => {
    const element = document.getElementById(fieldName);
    if (element && element.value) {
      formData[fieldName] = element.value;
    }
  });
  
  if (Object.keys(formData).length > 0) {
    localStorage.setItem('contactFormData', JSON.stringify(formData));
  }
}

// Observer para animaciones cuando los elementos entran en vista
function addAnimationObserver() {
  const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
  };
  
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.style.opacity = '1';
        entry.target.style.transform = 'translateY(0)';
      }
    });
  }, observerOptions);
  
  // Observar elementos que necesitan animación
  document.querySelectorAll('.contact-info, .business-hours, .social-media').forEach(el => {
    el.style.opacity = '0';
    el.style.transform = 'translateY(20px)';
    el.style.transition = 'all 0.6s ease-out';
    observer.observe(el);
  });
}

// Función para limpiar localStorage si es necesario
function clearStoredData() {
  localStorage.removeItem('contactFormData');
  showTemporaryMessage('Datos guardados eliminados', 'info');
}

// Función para exportar datos del formulario (útil para testing)
function exportFormData() {
  const formData = {
    name: document.getElementById('name').value,
    email: document.getElementById('email').value,
    subject: document.getElementById('subject').value,
    message: document.getElementById('message').value,
    timestamp: new Date().toISOString()
  };
  
  console.log('Datos del formulario:', formData);
  return formData;
}

// Eventos de teclado para mejorar UX
document.addEventListener('keydown', function(event) {
  // Enviar formulario con Ctrl+Enter
  if ((event.ctrlKey || event.metaKey) && event.key === 'Enter') {
    if (formState.isValid && !formState.isSubmitting) {
      handleFormSubmit(event);
    }
  }
  
  // Limpiar formulario con Ctrl+R (prevenir recarga)
  if ((event.ctrlKey || event.metaKey) && event.key === 'r') {
    event.preventDefault();
    if (confirm('¿Estás seguro de que quieres limpiar el formulario?')) {
      resetForm();
    }
  }
});

// Detectar si el usuario está abandonando la página con datos sin guardar
window.addEventListener('beforeunload', function(event) {
  if (formState.fields.name.value || formState.fields.email.value || formState.fields.message.value) {
    event.preventDefault();
    event.returnValue = '¿Estás seguro de que quieres salir? Los datos del formulario se guardarán automáticamente.';
    saveFormData();
  }
});

// Funciones para exponer globalmente (útil para debugging)
window.contactForm = {
  validate: () => validateName() && validateEmail() && validateSubject() && validateMessage(),
  reset: resetForm,
  export: exportFormData,
  clearStored: clearStoredData,
  getState: () => formState
};