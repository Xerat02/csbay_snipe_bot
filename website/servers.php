<!DOCTYPE html>
<html lang="en" class="scroll-smooth">
  <head>
    <?php include "components/analytics.php";?>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>CSBAY Sniper</title>
    <link rel="icon" type="image/x-icon" href="media/csbay_favi.png" />
    <!--Google fonts-->
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap"
      rel="stylesheet"
    />
    <!-- Tailwind CSS -->
    <link href="src/output.css" rel="stylesheet" />
  </head>
  <body class="bg-[#08090A] text-white font-unbuntu overflow-x-hidden">
      <?php include "components/header.php";?>
      <!-- Hero section -->
      <section class="space-y-12 text-center lg:text-left">
        <h1 class="text-4xl font-bold mb-8">Servers that use snipe bot</h1>
        <p id="server-count" class="text-lg font-medium mb-8"></p>
        <!-- Server count -->
        <div
          id="server-list"
          class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
        >
          <!-- Server items will be inserted here by JavaScript -->
        </div>
      </section>

      <?php include "components/footer.php";?>
    </div>
    <script>
      document.addEventListener("DOMContentLoaded", () => {
        fetch("https://api.csbay.org/servers")
          .then((response) => response.json())
          .then((data) => {
            const serverList = document.getElementById("server-list");
            const serverCount = document.getElementById("server-count");

            // Update server count
            serverCount.textContent = `Total Servers: ${data.length}`;

            // Populate the server list
            serverList.innerHTML = data
              .map(
                (server) => `
              <div class="bg-[#1e1e1e] p-4 rounded-lg shadow-lg text-center flex flex-col items-center justify-between rounded-2xl border-2 border-[#272c31]">
                <div class="w-full h-32 bg-gray-800 flex items-center justify-center rounded-lg overflow-hidden mb-4">
                  ${
                    server.icon
                      ? `<img src="${server.icon}" alt="${server.name} icon" class="w-full object-cover" />`
                      : `<span class="text-gray-400 text-lg">No Image</span>`
                  }
                </div>
                <h2 class="text-xl font-semibold mb-2">${server.name}</h2>
                <p class="text-sm text-gray-400">Members: ${
                  server.member_count
                }</p>
                <a href="${
                  server.server_link ? server.server_link : "#"
                }" class="mt-4 px-4 py-2 rounded-lg text-white ${
                  server.server_link
                    ? "bg-blue-500 hover:bg-blue-600"
                    : "bg-gray-500 cursor-not-allowed"
                }">${server.server_link ? "Join Server" : "Cannot Join"}</a>
              </div>
            `
              )
              .join("");
          })
          .catch((error) => console.error("Error fetching data:", error));
      });

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
    </script>
  </body>
</html>
