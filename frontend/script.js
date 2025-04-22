document.addEventListener("DOMContentLoaded", async () => {
  const carsContainer = document.querySelector("#carGrid");  // Здесь меняем на #carGrid

  try {
    const response = await fetch("http://127.0.0.1:8000/cars/all-cars", {
      method: "GET",
      headers: {
        "accept": "application/json"
      }
    });

    if (!response.ok) {
      throw new Error("Ошибка сети или сервера");
    }

    const cars = await response.json();
    carsContainer.innerHTML = "";  // Очистка контейнера перед выводом новых данных

    // Процесс отображения машин
    cars.forEach(car => {
      const carElement = document.createElement("div");

      // Формируем правильный путь для фото
      const photoUrl = car.car_photo
        ? `http://127.0.0.1:8000/cars/${car.car_photo.replace(/\\/g, '/')}`
        : "https://dummyimage.com/300x200/cccccc/000000&text=Нет+фото";

      // Заполнение данных о машине, меняем местами фото и текст
      carElement.innerHTML = `
        <div class="car-card">
          <img src="${photoUrl}" alt="Фото ${car.car_name}" width="300">
          <div class="car-card-content">
            <h3>${car.car_name} (${car.car_year})</h3>
            <p>Цена: ${car.car_price} $</p>
            <p>Компания: ${car.car_company}</p>
            <p>Цвет: ${car.car_color}</p>
            <p>Пробег: ${car.car_mileage} км</p>
            <button class="btn btn-primary" onclick="showCarDetails(${car.car_id})">Подробнее</button>
          </div>
        </div>
      `;
      carsContainer.appendChild(carElement);
    });
  } catch (error) {
    console.error("Ошибка при получении данных:", error);
  }
});

// Функция для отображения деталей машины
function showCarDetails(carId) {
  window.location.href = `page.html?car_id=${carId}`;
}

// Навигация для мобильных устройств
document.querySelector('.nav-toggle').addEventListener('click', () => {
  document.querySelector('.nav-links').classList.toggle('active');
});

// Закрытие меню при клике на ссылку
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelector('.nav-links').classList.remove('active');
  });
});



// Navigation toggle


document.querySelector('.nav-toggle').addEventListener('click', () => {
  document.querySelector('.nav-links').classList.toggle('active');
});

// Close mobile menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
  link.addEventListener('click', () => {
    document.querySelector('.nav-links').classList.remove('active');
  });
});

// Render car cards
function renderCars(carsToRender) {
  const carGrid = document.getElementById('carGrid');
  carGrid.innerHTML = carsToRender.map(car => `
    <div class="car-card">
      <img src="${car.image}" alt="${car.name}">
      <div class="car-card-content">
        <h3>${car.name}</h3>
        <p>${car.description}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 1rem;">
          <span style="font-weight: bold; color: var(--primary);">${car.price}</span>
          <button class="btn btn-primary" onclick="showCarDetails(${car.id})">Подробнее</button>
        </div>
      </div>
    </div>
  `).join('');
}

// Filter cars
function filterCars() {
  const searchTerm = document.querySelector('.search-input').value.toLowerCase();
  const selectedBrand = document.querySelector('.filter-select').value;
  
  const filteredCars = cars.filter(car => {
    const matchesSearch = car.name.toLowerCase().includes(searchTerm) ||
                         car.description.toLowerCase().includes(searchTerm);
    const matchesBrand = !selectedBrand || car.brand === selectedBrand;
    return matchesSearch && matchesBrand;
  });
  
  renderCars(filteredCars);
}

// Add event listeners for filters
document.querySelector('.search-input').addEventListener('input', filterCars);
document.querySelector('.filter-select').addEventListener('change', filterCars);

// Contact form submission



