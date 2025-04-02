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
    <meta
      property="og:description"
      content="Make MONEY by buying CS2 skins. Our snipebot scans thousands of offers across markets for you and shows you the best and most attractive deals."
    />
    <meta
      property="og:image"
      content="https://csbay.net/sniper/media/hero_image.png"
    />
    <meta property="og:site_name" content="CSBAY Sniper" />

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:url" content="https://csbay.net/sniper" />
    <meta name="twitter:title" content="CSBAY Sniper" />
    <meta
      name="twitter:description"
      content="Make MONEY by buying CS2 skins. Our snipebot scans thousands of offers across markets for you and shows you the best and most attractive deals."
    />
    <meta
      name="twitter:image"
      content="https://csbay.net/sniper/media/hero_image.png"
    />

    <!-- Instagram (uses Open Graph tags) -->
    <meta property="og:type" content="website" />
    <meta property="og:url" content="https://csbay.net/sniper" />
    <meta property="og:title" content="CSBAY Sniper" />
    <meta
      property="og:description"
      content="Make MONEY by buying CS2 skins. Our snipebot scans thousands of offers across markets for you and shows you the best and most attractive deals."
    />
    <meta
      property="og:image"
      content="https://csbay.net/sniper/media/hero_image.png"
    />

    <link href="src/output.css" rel="stylesheet" />
  </head>
  <body class="bg-[#08090A] text-white font-unbuntu overflow-x-hidden">
      <?php include "components/header.php";?>
      <!--Hero section-->
      <section class="text-center lg:text-left space-y-12">
        <h1 class="text-[18px] lg:text-[24px] w-full">
          1) Add Sniper to your Discord server using
          <strong>"Add to Discord"</strong> button.
        </h1>
        <img
          src="media/sniper-tutorial/1.png"
          alt=""
          class="mx-auto rounded-2xl"
        />

        <h1 class="text-[18px] lg:text-[24px] w-full">
          2) Select the server where you want Sniper to be.
        </h1>
        <img
          src="media/sniper-tutorial/2.png"
          alt=""
          class="mx-auto rounded-2xl"
        />
        <h1 class="text-[18px] lg:text-[24px] w-full">
          3) Make sure that the Sniper has
          <strong>"Send Messages"</strong> permission.
        </h1>
        <img
          src="media/sniper-tutorial/3.png"
          alt=""
          class="mx-auto rounded-2xl"
        />
        <h1 class="text-[18px] lg:text-[24px] w-full">
          4) Make a new category called SKINS SNIPE or something like that. In
          that category create 6 channels (Info, Low, Mid, High, Stats)
        </h1>
        <img
          src="media/sniper-tutorial/4.png"
          alt=""
          class="mx-auto rounded-2xl"
        />
        <h1 class="text-[18px] lg:text-[24px] w-full">
          <span class="font-bold"
            >5) Setup each channel using "/" commands.</span
          >
          <br />
          <span class="font-normal"
            >/send_info - sends a message with informations about the
            Sniper</span
          >
          <br />
          <span class="font-normal"
            >/setup_channel - sets a channel for low/mid/high/best tiers (one
            foreach channel)</span
          >
          <br />
          <span class="font-normal"
            >/remove_channel - stops Sniper's activity in that channel</span
          >
        </h1>
        <div class="grid grid-cols-3 gap-5">
          <img
            src="media/sniper-tutorial/low.png"
            alt=""
            class="mx-auto rounded-2xl"
          />
          <img
            src="media/sniper-tutorial/mid.png"
            alt=""
            class="mx-auto rounded-2xl"
          />
          <img
            src="media/sniper-tutorial/high.png"
            alt=""
            class="mx-auto rounded-2xl"
          />
          <img
            src="media/sniper-tutorial/mid.png"
            alt=""
            class="mx-auto rounded-2xl"
          />
          <img
            src="media/sniper-tutorial/best.png"
            alt=""
            class="mx-auto rounded-2xl"
          />
        </div>
      </section>
      <?php include "components/footer.php";?>
    </div>
    <script>
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
