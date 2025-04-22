document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contactForm');
    console.log('contactForm:', contactForm); // Отладочное сообщение
  
    if (contactForm) {
      contactForm.addEventListener('submit', async (e) => {
        e.preventDefault();
  
        // Получаем данные из формы с использованием FormData
        const formData = new FormData(contactForm);
        const data = {
          request_name: formData.get('name'),
          request_email: formData.get('email'),
          request_phone: formData.get('phone'),
          request_message: formData.get('message')
        };
  
        try {
          // Отправляем POST-запрос на сервер
          const response = await fetch("http://127.0.0.1:8000/website_requests/add/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "accept": "application/json"
            },
            body: JSON.stringify(data)
          });
  
          if (!response.ok) {
            throw new Error("Ошибка при отправке запроса");
          }
  
          const result = await response.json();
          alert('Сообщение отправлено! Мы свяжемся с вами в ближайшее время.');
          e.target.reset(); // Очищаем форму после успешной отправки
        } catch (error) {
          console.error("Ошибка при отправке данных:", error);
          alert('Произошла ошибка при отправке сообщения. Пожалуйста, попробуйте еще раз.');
        }
      });
    } else {
      console.error('Элемент с id "contactForm" не найден.');
    }
  });
  