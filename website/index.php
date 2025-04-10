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

    <!-- Open Graph / Facebook -->
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://csbay.net/sniper" />
    <meta property="og:title" content="CSBAY Sniper" />
    <meta property="og:description" content="Make MONEY by buying CS2 skins. Our snipebot scans thousands of offers across markets for you and shows you the best and most attractive deals." />
    <meta property="og:image" content="https://csbay.net/sniper/media/hero_image.png" />
    <meta property="og:site_name" content="CSBAY Sniper" />

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:url" content="https://csbay.net/sniper" />
    <meta name="twitter:title" content="CSBAY Sniper" />
    <meta name="twitter:description" content="Make MONEY by buying CS2 skins. Our snipebot scans thousands of offers across markets for you and shows you the best and most attractive deals." />
    <meta name="twitter:image" content="https://csbay.net/sniper/media/hero_image.png" />

    <!-- Instagram (uses Open Graph tags) -->
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://csbay.net/sniper" />
    <meta property="og:title" content="CSBAY Sniper" />
    <meta property="og:description" content="Make MONEY by buying CS2 skins. Our snipebot scans thousands of offers across markets for you and shows you the best and most attractive deals." />
    <meta property="og:image" content="https://csbay.net/sniper/media/hero_image.png" />

    <link href="src/output.css" rel="stylesheet" />
  </head>
  <body class="bg-[#08090A] text-white font-unbuntu overflow-x-hidden">
    <?php include "components/header.php";?>
    <!--Hero section-->
    <section>
      <div class="flex flex-col lg:flex-row justify-between items-center my-6">
        <div>
          <h1 class="text-[24px] lg:text-[42px] font-bold mb-5 text-center lg:text-left">
            Make
            <span
              class="text-transparent bg-clip-text bg-gradient-to-tr from-[#0047FF] to-[#726FF9]"
              >MONEY</span
            >
            by buying CS2 skins
          </h1>
          <div class="w-full">
            <p
              class="text-[12px] lg:text-[18px] text-[#BDBDBD] mb-5 lg:max-w-[75%] text-center lg:text-left"
            >
              Our snipebot scans thousands of offers across markets for you and
              shows you the best and most attractive deals
            </p>
          </div>
          <a
            href="https://discord.com/oauth2/authorize?client_id=1104871916940050542&scope=bot&permissions=277025507328"
            target="_blank"
            class="w-full mx-auto lg:mx-0 lg:w-max px-6 py-2 bg-gradient-to-tr from-[#2655FD] to-[#4D62FB] rounded-2xl flex justify-center items-center font-bold hover:scale-105 transition-all active::animate-ping"
          >
            <span class="mr-5 text-[12px] lg:text-[18px]">Add to Discord</span>
            <img
              src="media/discord_icon.png"
              alt="Discord icon"
              class="h-[40px] w-[40px]"
            />
          </a>
        </div>
        <img src="media/hero_image.png" alt="Hero image" srcset="" />
      </div>
    </section>
    <!--Key Features and Benefits section-->
    <section
      class="flex flex-col justify-center text-center lg:text-left space-y-24"
      id="features"
    >
      <div
        class="flex lg:flex-row flex-col lg:justify-between items-center mb-5"
      >
        <img
          src="media/showcase_image.png"
          alt="Showcase image"
          srcset=""
          class="hidden lg:block w-[650px] h-[380px]"
        />
        <div class="flex-1 lg:p-12">
          <h1 class="text-[24px] lg:text-[42px] font-bold mb-2">
            Snipe your dream knife
          </h1>
          <div>
            <p
              class="text-[12px] lg:text-[18px] text-[#BDBDBD] mb-2"
            >
              It has never been easier to get your dreamed knife for the best price possible
            </p>
          </div>
        </div>
        <img
          src="media/showcase_image.png"
          alt="Showcase image"
          srcset=""
          class="lg:hidden block w-[650px] h-[250px]"
        />
      </div>
      <div class="flex lg:flex-row flex-col lg:justify-between items-center">
        <div class="flex-1 lg:py-12 lg:pr-12">
          <h1 class="text-[24px] lg:text-[42px] font-bold mb-2">
            Instantly flip it
          </h1>
          <div>
            <p
              class="text-[12px] lg:text-[18px] text-[#BDBDBD] mb-2"
            >
              You can instantly flip it on buff163 or any market of your choice
            </p>
          </div>
        </div>
        <video class="w-[650px] rounded-2xl flex" autoplay muted loop>
          <source src="media/showcase_video.mp4" type="video/mp4">
        </video> 
      </div>
    </section>
    <!--How it works-->
    <section class="flex flex-col lg:flex-row justify-center lg:justify-between items-center" id="how_it_works">
      <div class="flex-1 text-center lg:text-left">
        <h1 class="text-[24px] lg:text-[42px] font-bold mb-2">
          How it works
        </h1>
        <div>
          <p
            class="text-[12px] lg:text-[18px] text-[#BDBDBD] lg:max-w-[60%] mb-2"
          >
            Step-by-step process from selecting your skin to completing the transaction
          </p>
        </div>
      </div>
      <div class="flex-1 space-y-16">
        <div class="flex flex-row items-center">
          <div
            class="relative flex-shrink-0 w-[25px] lg:w-[35px] h-[25px] lg:h-[35px] bg-[#3159FD] rounded-full mr-8"
          >
            <div
              class="absolute top-[100%] -translate-y- left-1/2 -translate-x-1/2 w-[3px] h-[190px] bg-[#242425] mr-8"
            ></div>
          </div>

          <div
            class="flex items-center w-full px-5 py-3 lg:py-8 bg-[#181B1E] rounded-2xl border-2 border-[#272c31]"
          >
            <img
              src="media/scan_icon.png"
              alt="Hero image"
              srcset=""
              class="w-[40px] lg:w-[50px] mr-5"
            />
            <div>
              <h1 class="text-[18px] lg:text-[24px] w-full">Market Scan</h1>
              <p class="text-[12px] lg:text-[18px] text-[#BDBDBD]">
                Sniper scans thousands of offers across markets
              </p>
            </div>
          </div>
        </div>
        <div class="flex flex-row items-center">
          <div
            class="relative flex-shrink-0 w-[25px] lg:w-[35px] h-[25px] lg:h-[35px] bg-[#3159FD] rounded-full mr-8"
          >
            <div
              class="absolute top-[100%] -translate-y- left-1/2 -translate-x-1/2 w-[3px] h-[190px] bg-[#242425] mr-8"
            ></div>
          </div>

          <div
            class="flex items-center w-full px-5 py-3 lg:py-8 bg-[#181B1E] rounded-2xl border-2 border-[#272c31]"
          >
            <img
              src="media/bargain_icon.png"
              alt="Hero image"
              srcset=""
              class="w-[40px] lg:w-[50px] mr-5"
            />
            <div>
              <h1 class="text-[18px] lg:text-[24px] w-full">Save a Bargain Deal</h1>
              <p class="text-[12px] lg:text-[18px] text-[#BDBDBD]">
                The sniper efficiently identifies a potential good deal
              </p>
            </div>
          </div>
        </div>
        <div class="flex flex-row items-center">
          <div
            class="relative flex-shrink-0 w-[25px] lg:w-[35px] h-[25px] lg:h-[35px] bg-[#3159FD] rounded-full mr-8"
          >
            <div
              class="absolute top-[100%] -translate-y- left-1/2 -translate-x-1/2 w-[3px] h-[155px] lg:h-[190px] bg-[#242425] mr-8"
            ></div>
          </div>

          <div
            class="flex items-center w-full px-5 py-3 lg:py-8 bg-[#181B1E] rounded-2xl border-2 border-[#272c31]"
          >
            <img
              src="media/market_analyze_icon.png"
              alt="Hero image"
              srcset=""
              class="w-[40px] lg:w-[50px] mr-5"
            />
            <div>
              <h1 class="text-[18px] lg:text-[24px] w-full">Analyze Deal</h1>
              <p class="text-[12px] lg:text-[18px] text-[#BDBDBD]">
                Sniper compares the item's price with Buff 163
              </p>
            </div>
          </div>
        </div>
        <div class="flex flex-row items-center">
          <div
            class="relative flex-shrink-0 w-[25px] lg:w-[35px] h-[25px] lg:h-[35px] bg-[#3159FD] rounded-full mr-8"
          >
          </div>
          <div
            class="flex items-center w-full px-5 py-3 lg:py-8 bg-[#181B1E] rounded-2xl border-2 border-[#272c31]"
          >
            <img
              src="media/notification_icon.png"
              alt="Hero image"
              srcset=""
              class="w-[40px] lg:w-[50px] mr-5"
            />
            <div>
              <h1 class="text-[18px] lg:text-[24px] w-full">Discord Notification</h1>
              <p class="text-[12px] lg:text-[18px] text-[#BDBDBD]">
                Sniper sends profitable and low-risk deal to Discord
              </p>
            </div>
          </div>
        </div>
    </section>
    <!--Supported Marketplaces & Trading Sites-->
    <section id="supported_marketplaces">
      <h1 class="text-[24px] lg:text-[42px] w-full text-center mb-5">
        Supported Marketplaces
      </h1>
      <div
        class="flex flex-row overflow-x-scroll no-scrollbar space-x-5 p-5"
        id="scroll-container"
      >
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/shadowpay.png"
            alt="Shadowpay"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">
            Shadowpay
          </h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/gamerpay.png"
            alt="Gamerpay"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">
            Gamerpay
          </h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/csmoney.png"
            alt="CSMoney"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">CSMoney</h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/whitemarket.png"
            alt="Whitemarket"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">
            Whitemarket
          </h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/buffmarket.jpg"
            alt="Buffmarket"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">
            Buffmarket
          </h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/mannco.png"
            alt="Mannco"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">Mannco</h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/marketcsgo.png"
            alt="MarketCSGO"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">
            MarketCSGO
          </h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/skinbaron.png"
            alt="Skinbaron"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">
            Skinbaron
          </h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/skinbid.jpg"
            alt="Skinbid"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">Skinbid</h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/skinport.png"
            alt="Skinport"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">
            Skinport
          </h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/skinwallet.png"
            alt="Skinwallet"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">
            Skinwallet
          </h2>
        </div>
        <div
          class="flex-shrink-0 flex flex-col justify-center items-center bg-[#181B1E] h-[200px] lg:h-[300px] w-[200px] lg:w-[300px] rounded-2xl px-8 border-2 border-[#272c31]"
        >
          <img
            src="media/waxpeer.png"
            alt="Waxpeer"
            class="w-[100px] lg:w-[150px] h-[100px] lg:h-[150px] mx-auto mb-3 lg:mb-5"
          />
          <h2 class="text-[18px] lg:text-[24px] w-full text-center">Waxpeer</h2>
        </div>
      </div>
    </section>
    <!--Support server-->
    <section id="support-server">
      <div class="bg-[#181B1E] p-6 lg:p-12 rounded-2xl border-2 border-[#272c31]">
        <h1 class="text-[24px] lg:text-[42px] w-full">
          Get in touch with our support
        </h1>
        <p class="text-[12px] lg:text-[18px] text-[#BDBDBD] mb-5">
          We will do our best to get you an answer/response as fast as possible.
        </p>
        <a
        href="https://discord.com/invite/csbay-cs2-trading-642813124629757953"
        target="_blank"
        class="w-full lg:w-max px-6 py-2 bg-gradient-to-tr from-[#2655FD] to-[#4D62FB] rounded-2xl flex justify-center items-center font-bold mr-5 hover:scale-105 transition-all active::animate-ping"
        >
        <span class="mr-5 text-[12px] lg:text-[18px]">Join Our Discord</span>
          <img
            src="media/discord_icon.png"
            alt="Discord icon"
            class="h-[40px] w-[40px]"
          />
        </a>
      </div>
    </section>
    <!--FAQ-->
    <section id="faq">
      <h1 class="text-[24px] lg:text-[42px] w-full text-center mb-5">FAQ</h1>
      <div>
        <div
          class="relative w-full lg:w-[55%] mx-auto h-[90px] lg:h-[120px] cursor-pointer"
          id="faq1-question"
          onclick="toggleFAQ('faq1')"
        >
          <div class="absolute left-5 top-1/2 transform -translate-y-1/2">
            <img
              id="faq1-arrow"
              src="media/arrow.png"
              alt="Arrow"
              class="transition-transform duration-300 w-[40px] lg:w-[60px]"
            />
          </div>
          <h2
            class="text-[18px] lg:text-[24px] text-center absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2"
          >
            What is SnipeBot and how does it work?
          </h2>
        </div>
        <div class="hidden p-5" id="faq1">
          <p class="text-[12px] lg:text-[18px] text-[#BDBDBD] text-center">
            Sniper is a Discord bot that scans multiple CS2-related markets and show you bargain items
          </p>
        </div>

        <div
          class="relative w-full lg:w-[55%] mx-auto h-[90px] lg:h-[120px] cursor-pointer"
          id="faq2-question"
          onclick="toggleFAQ('faq2')"
        >
          <div class="absolute left-5 top-1/2 transform -translate-y-1/2">
            <img
              id="faq2-arrow"
              src="media/arrow.png"
              alt="Arrow"
              class="transition-transform duration-300 w-[40px] lg:w-[60px]"
            />
          </div>
          <h2
            class="text-[18px] lg:text-[24px] text-center absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2"
          >
            How does SnipeBot compare prices?
          </h2>
        </div>
        <div class="hidden p-5" id="faq2">
          <p class="text-[12px] lg:text-[18px] text-[#BDBDBD] text-center">
            Sniper compare all markets to Buff163
          </p>
        </div>

        <div
          class="relative w-full lg:w-[55%] mx-auto h-[90px] lg:h-[120px] cursor-pointer"
          id="faq3-question"
          onclick="toggleFAQ('faq3')"
        >
          <div class="absolute left-5 top-1/2 transform -translate-y-1/2">
            <img
              id="faq3-arrow"
              src="media/arrow.png"
              alt="Arrow"
              class="transition-transform duration-300 w-[40px] lg:w-[60px]"
            />
          </div>
          <h2
            class="text-[18px] lg:text-[24px] text-center absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2"
          >
            What factors does SnipeBot analyze in each deal?
          </h2>
        </div>
        <div class="hidden p-5" id="faq3">
          <p class="text-[12px] lg:text-[18px] text-[#BDBDBD] text-center">
            Sniper analyze risk factor, potential profit and discount
          </p>
        </div>

        <div
          class="relative w-full lg:w-[55%] mx-auto h-[90px] lg:h-[120px] cursor-pointer"
          id="faq4-question"
          onclick="toggleFAQ('faq4')"
        >
          <div class="absolute left-5 top-1/2 transform -translate-y-1/2">
            <img
              id="faq4-arrow"
              src="media/arrow.png"
              alt="Arrow"
              class="transition-transform duration-300 w-[40px] lg:w-[60px]"
            />
          </div>
          <h2
            class="text-[18px] lg:text-[24px] text-center absolute top-1/2 left-1/2 transform -translate-y-1/2 -translate-x-1/2"
          >
            How often does SnipeBot update its data?
          </h2>
        </div>
        <div class="hidden p-5" id="faq4">
          <p class="text-[12px] lg:text-[18px] text-[#BDBDBD] text-center">
            Sniper gradually updates data every minute.
          </p>
        </div>
      </div>
    </section>
    <?php include "components/footer.php";?>
    </div>


    <script src="https://unpkg.com/scrollreveal"></script>
    <script>
      function toggleFAQ(faqId) {
        const content = document.getElementById(faqId);
        const arrow = document.getElementById(faqId + "-arrow");
        const question = document.getElementById(faqId + "-question");
        if (content.classList.contains("hidden")) {
          content.classList.remove("hidden");
          arrow.style.transform = "rotate(-90deg)";
        } else {
          content.classList.add("hidden");
          arrow.style.transform = "rotate(0deg)";
        }
      }

      const scrollContainer = document.getElementById("scroll-container");

      let scrollAmount = 0;
      const scrollStep = 2;

      function autoScroll() {
        scrollAmount += scrollStep;
        if (
          scrollAmount >=
          scrollContainer.scrollWidth - scrollContainer.clientWidth
        ) {
          scrollAmount = 0;
        }
        scrollContainer.scrollTo({
          left: scrollAmount,
          behavior: "smooth",
        });
      }
      
      setInterval(autoScroll, 20);

      function mobile_nav(){
        const NAV = document.getElementById("mobile_menu");
        if (NAV.classList.contains("hidden")){
          NAV.classList.remove("hidden")
          NAV.classList.add("flex")
        }
        else {
          NAV.classList.add("hidden")
          NAV.classList.remove("flex")
        }
      }
    </script>
  </body>
</html>
