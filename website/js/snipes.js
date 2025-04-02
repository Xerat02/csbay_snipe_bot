function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleString();
}

function formatRelativeTime(lastUpdateTime) {
  const currentTime = new Date();
  const diffInSeconds = Math.floor((currentTime - lastUpdateTime) / 1000);
  const diffInMinutes = Math.floor(diffInSeconds / 60);
  const diffInHours = Math.floor(diffInMinutes / 60);
  const diffInDays = Math.floor(diffInHours / 24);

  if (diffInDays > 0) {
    return `${diffInDays} day${diffInDays > 1 ? "s" : ""} ago`;
  } else if (diffInHours > 0) {
    return `${diffInHours} hour${diffInHours > 1 ? "s" : ""} ago`;
  } else if (diffInMinutes > 0) {
    return `${diffInMinutes} minute${diffInMinutes > 1 ? "s" : ""} ago`;
  } else {
    return `${diffInSeconds} second${diffInSeconds > 1 ? "s" : ""} ago`;
  }
}

function updatePulseDotsAndTime() {
  const pulseDots = document.querySelectorAll("#pulse-dot");
  const offerTimes = document.querySelectorAll("#offer-created");

  if (!pulseDots.length && !offerTimes.length) {
    return;
  }

  pulseDots.forEach((pulseDot) => {
    const updateTime = new Date(pulseDot.getAttribute("data-update-time"));
    const currentTime = new Date();
    const diffInHours = Math.floor(
      (currentTime.getTime() - updateTime.getTime()) / (1000 * 60 * 60)
    );

    let colorClass = "bg-green-500";
    if (diffInHours <= 3) {
      colorClass = "bg-green-500";
    } else if (diffInHours <= 6) {
      colorClass = "bg-yellow-500";
    } else if (diffInHours <= 12) {
      colorClass = "bg-orange-500";
    } else {
      colorClass = "bg-red-500";
    }

    pulseDot.innerHTML = `
  <span class="relative flex h-4 w-4">
    <span class="animate-ping absolute inline-flex h-full w-full rounded-full ${colorClass} opacity-75"></span>
    <span class="relative inline-flex rounded-full h-4 w-4 ${colorClass}" title="Buff data was updated ${formatRelativeTime(
      updateTime
    )}"></span>
  </span>
`;
  });
  offerTimes.forEach((offerTime) => {
    const offerCreatedTime = new Date(
      offerTime.getAttribute("data-created-time")
    );
    offerTime.innerHTML = `Offer created ${formatRelativeTime(
      new Date(offerCreatedTime)
    )}`;
  });
}

// Function to get risk text and CSS class
function getRiskTextAndClass(riskFactor, sellNum) {
  const riskLevels = ["Low", "Medium", "High", "Very High"];
  const colors = [
    "bg-green-500",
    "bg-yellow-500",
    "bg-orange-500",
    "bg-red-500",
  ];

  // Determine the risk level and corresponding color
  const level = riskLevels[Math.min(riskFactor, 3)];
  const riskClass = colors[Math.min(riskFactor, 3)];

  return { text: `${level} (${sellNum} on sale)`, class: riskClass };
}

// Function to get discount CSS class and icon
function getBuffDiscountClassAndIcon(discount) {
  if (discount >= 15) return { class: "text-green-500 font-bold", icon: "🟩" };
  if (discount >= 10) return { class: "text-yellow-500 font-bold", icon: "🟨" };
  if (discount >= 6.5)
    return { class: "text-orange-500 font-bold", icon: "🟧" };
  return { class: "text-red-500 font-bold", icon: "🟥" };
}

function getUniqueItems(arr1, arr2) {
  const ids2 = new Set(arr2.map((item) => item._id));

  return arr1.filter((item) => !ids2.has(item._id));
}

// Variables to store the filter values
let currentRiskFactor = null;
let currentBuffDiscount = null;
let currentMinPrice = null;
let currentMaxPrice = null;

let previous_data = null;

// Function to update filters from the UI
function updateFilters() {
  currentRiskFactor = document.getElementById("risk-factor").value;
  currentBuffDiscount = document.getElementById("buff-discount").value;
  currentMinPrice = document.getElementById("min-price").value;
  currentMaxPrice = document.getElementById("max-price").value;

  console.log("Risk Factor:", currentRiskFactor);
  console.log("Buff Discount:", currentBuffDiscount);
  console.log("Min Price:", currentMinPrice);
  console.log("Max Price:", currentMaxPrice);

  document.getElementById("data-grid").textContent = "";
  previous_data = null;
  fetchData();
}

// Function to update the discount label based on slider value
function updateDiscountLabel(value) {
  document.getElementById("discount-label").textContent = `${value}%`;
}

// Function to fetch and display data
async function fetchData() {
  const queryParams = new URLSearchParams();

  if (currentRiskFactor) queryParams.append("risk_factor", currentRiskFactor);

  // Use the currentBuffDiscount with the slider value
  if (currentBuffDiscount)
    queryParams.append("buff_discount", currentBuffDiscount);

  if (currentMinPrice) queryParams.append("min_price", currentMinPrice);
  if (currentMaxPrice) queryParams.append("max_price", currentMaxPrice);

  const queryString = queryParams.toString();
  const apiUrl = `https://api.csbay.org/snipes?${
    queryString ? queryString : ""
  }`;

  try {
    const response = await fetch(apiUrl);
    const data = await response.json();

    const dataGrid = document.getElementById("data-grid");

    if (previous_data == null || previous_data[0]["_id"] != data[0]["_id"]) {
      let new_items = null;
      if (previous_data != null) {
        new_items = getUniqueItems(data, previous_data);
      } else {
        new_items = data;
      }

      new_items.forEach((item, index) => {
        const card = document.createElement("div");
        card.className =
          "border-2 border-[#272c31] bg-[#181b1ed0] p-4 rounded-lg shadow-lg transition-transform transform hover:!scale-105 scale-0 opacity-0";

        const riskInfo = getRiskTextAndClass(
          item.market_risk_factor,
          item.buff_item_sell_num
        );
        const discountInfo = getBuffDiscountClassAndIcon(item.buff_discount);

        const updateTime = new Date(item.buff_data_update_time);

        card.innerHTML = `
    <div class="relative">
      <div class="w-full relative inline-block">
        <div id="pulse-dot" class="absolute top-2 left-2 w-4 h-4 rounded-full" data-update-time="${updateTime.toISOString()}"></div>
        <img
          src="${item.market_logo}"
          alt="Market Logo"
          referrerpolicy="no-referrer"
          class="absolute top-2 right-2 w-8 h-8 object-cover rounded-lg"
          title="${item.market_name}"
        />
        <div class="absolute top-0 right-0 mt-12 mr-2 hidden group-hover:block bg-gray-700 text-white text-sm rounded py-1 px-2">
          ${item.market_name}
        </div>
        <img
          src="${item.buff_item_image}"
          alt="Item Image"
          class="w-1/2 mx-auto h-32 object-cover mb-4"
        />
        <a
          href="${item.market_link}"
          target="_blank"
          class="flex items-center w-full h-[70px] text-blue-400 text-lg font-semibold mb-2 hover:underline"
        >
          ${item.item_name}
        </a>
        <p id="risk_factor" class="w-full text-sm ${
          riskInfo.class
        } text-white px-2 py-1 rounded" >Risk Factor: ${riskInfo.text}</p>
        <p class="mt-4 w-full text-sm text-gray-300 buff-price">Buff Price: $<span id="buff_price">0</span></p>
        <p class="w-full text-sm text-gray-300 buff-price">Market Price: $<span id="market_price">0</span></p>
        <p class="w-full text-sm text-gray-300">Potential Profit: $<span id="potential_profit">0</span></p>
        <p class="w-full text-sm ${discountInfo.class}">Buff Discount: ${
          discountInfo.icon
        } <span id="buff_discount">0</span>%</p>
        <p class="w-full text-sm text-gray-300">Steam Discount: <span id="steam_discount">0</span>%</p>
        <p class="w-full text-sm text-gray-300" id="offer-created" data-created-time="${
          item.inserted_time
        }"></p>
        <div class="w-full mt-4 flex flex-col gap-2">
          <a
            href="${item.buff_item_link}"
            id="btn1"
            target="_blank"
            class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 w-full text-center"
          >
            Check Buff
          </a>
          <a
            href="${item.market_link}"
            id="btn2"
            target="_blank"
            class="bg-green-500 text-white px-4 py-2 rounded hover:bg-green-600 w-full text-center"
          >
            Buy Now
          </a>
        </div>
      </div>
    </div>
  `;
        //animations
        anime({
          targets: card,
          scale: [0, 1],
          opacity: [0, 1],
          duration: 400,
          easing: "linear",
          delay: index * 50,
        });

        //risk factor
        anime({
          targets: card.querySelector("#risk_factor"),
          scale: [0, 1],
          opacity: [0, 1],
          easing: "linear",
          duration: 400,
          delay: 500,
        });
        //buff price
        anime({
          targets: card.querySelector("#buff_price"),
          innerHTML: [0, item.buff_price],
          easing: "linear",
          round: 100,
          delay: 200,
        });
        //market price
        anime({
          targets: card.querySelector("#market_price"),
          innerHTML: [0, item.market_price],
          easing: "linear",
          round: 100,
          delay: 300,
        });
        //potential profit
        anime({
          targets: card.querySelector("#potential_profit"),
          innerHTML: [0, item.profit[0]],
          easing: "linear",
          round: 100,
          delay: 400,
        });
        //buff discount
        anime({
          targets: card.querySelector("#buff_discount"),
          innerHTML: [0, item.buff_discount],
          easing: "linear",
          round: 100,
          delay: 500,
        });
        //steam discount
        anime({
          targets: card.querySelector("#steam_discount"),
          innerHTML: [0, item.steam_discount],
          easing: "linear",
          round: 100,
          delay: 600,
        });
        //btn1
        anime({
          targets: card.querySelector("#btn1"),
          scale: [0, 1],
          opacity: [0, 1],
          duration: 400,
          easing: "linear",
          duration: 400,
          delay: 500,
        });
        //btn2
        anime({
          targets: card.querySelector("#btn2"),
          scale: [0, 1],
          opacity: [0, 1],
          duration: 400,
          easing: "linear",
          duration: 400,
          delay: 500,
        });

        if (previous_data == null) {
          dataGrid.append(card);
        } else {
          dataGrid.prepend(card);
          dataGrid.removeChild(dataGrid.lastChild);
        }
      });
      updatePulseDotsAndTime();
      previous_data = data;
    }
  } catch (error) {
    console.error("Error fetching data:", error);
  }
}

// Initialize filters and fetch data initially
updateFilters();
fetchData();

// Re-fetch data every 2 seconds
setInterval(fetchData, 2000);

function mobile_nav() {
  const NAV = document.getElementById("mobile_menu");
  if (NAV.classList.contains("hidden")) {
    NAV.classList.remove("hidden");
    NAV.classList.add("flex");
  } else {
    NAV.classList.add("hidden");
    NAV.classList.remove("flex");
  }
}
