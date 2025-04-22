document.addEventListener("DOMContentLoaded", async () => {
    const carDetailContainer = document.querySelector("#carDetailContainer");
    const urlParams = new URLSearchParams(window.location.search);
    const carId = urlParams.get("car_id");
  
    if (!carId) {
      carDetailContainer.innerHTML = "<p>Машина не найдена.</p>";
      return;
    }
  
    try {
      const response = await fetch(`http://127.0.0.1:8000/cars/get-car?car_id=${carId}`, {
        method: "GET",
        headers: {
          "accept": "application/json"
        }
      });
  
      if (!response.ok) {
        throw new Error("Ошибка сети или сервера");
      }
  
      const car = await response.json();
  
      // Формируем правильный путь для фото
      const photoUrl = car.car_photo
        ? `http://127.0.0.1:8000/cars/${car.car_photo.replace(/\\/g, '/')}`
        : "https://dummyimage.com/300x200/cccccc/000000&text=Нет+фото";
  
      // Заполнение деталей машины
      carDetailContainer.innerHTML = `
        <div class="car-photo">
          <img src="${photoUrl}" alt="Фото ${car.car_name}" width="500">
        </div>
        <div class="car-info">
          <h3>${car.car_name} (${car.car_year})</h3>
          <p><strong>Цена:</strong> ${car.car_price} $</p>
          <p><strong>Компания:</strong> ${car.car_company}</p>
          <p><strong>Цвет:</strong> ${car.car_color}</p>
          <p><strong>Пробег:</strong> ${car.car_mileage} км</p>
        </div>
      `;
    } catch (error) {
      console.error("Ошибка при получении данных:", error);
      carDetailContainer.innerHTML = "<p>Не удалось загрузить данные о машине.</p>";
    }
  });
  