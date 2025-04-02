<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
  <head>
    <?php include "components/analytics.php";?>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CSBAY Sniper</title>
    <link rel="icon" type="image/x-icon" href="media/csbay_favi.png" />
    <!-- Google fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700&display=swap"
      rel="stylesheet"
    />
    <link href="src/output.css" rel="stylesheet" />
    <script src="https://cdn.tailwindcss.com"></script>
  </head>
  <body class="bg-[#08090A] text-white font-unbuntu overflow-x-hidden">
      <?php include "components/header.php";?>
      <!-- Filter section -->
      <div
        class="bg-[#181b1ed0] p-4 rounded-lg mb-10 border-2 border-[#272c31]"
      >
        <h2 class="text-xl font-bold mb-4">Filters</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <!-- Risk Factor Filter -->
          <div>
            <label for="risk-factor" class="block text-sm font-medium mb-2"
              >Risk Factor</label
            >
            <select
              id="risk-factor"
              class="w-full p-2 border rounded-lg bg-[#272c31] text-white"
              onchange="updateFilters()"
            >
              <option value="">All</option>
              <option value="0">Low</option>
              <option value="1">Medium</option>
              <option value="2">High</option>
              <option value="3">Very High</option>
            </select>
          </div>

          <!-- Buff Discount Filter -->
          <div>
            <label for="buff-discount" class="block text-sm font-medium mb-2"
              >Buff Discount (Greater than)</label
            >
            <input
              type="range"
              id="buff-discount"
              min="0"
              max="100"
              step="0.5"
              value="0"
              class="w-full p-2 border rounded-lg bg-[#272c31] text-white"
              onchange="updateFilters()"
              oninput="updateDiscountLabel(this.value)"
            />
            <span id="discount-label" class="text-sm text-gray-300 mt-2 block"
              >0%</span
            >
          </div>

          <!-- Market Price Filter -->
          <div>
            <label for="market-price" class="block text-sm font-medium mb-2"
              >Market Price Range</label
            >
            <input
              type="number"
              id="min-price"
              placeholder="Min"
              min="0"
              class="w-full mb-2 p-2 border rounded-lg bg-[#272c31] text-white shadow-xl"
              onchange="updateFilters()"
            />
            <input
              type="number"
              id="max-price"
              placeholder="Max"
              min="1"
              class="w-full p-2 border rounded-lg bg-[#272c31] text-white shadow-xl"
              onchange="updateFilters()"
            />
          </div>
        </div>
      </div>

      <!-- Data display section -->
      <div
        id="data-grid"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6"
      >
        <!-- Cards will be inserted here -->
      </div>
    </div>
    <?php include "components/footer.php";?>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>
    <script src="js/snipes.js"></script>
  </body>
</html>
