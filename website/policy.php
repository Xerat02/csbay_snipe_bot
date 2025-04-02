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
      <section class="space-y-12 text-center lg:text-left">
        <h2 class="text-2xl font-extrabold">Privacy Policy</h2>
        <p>Effective Date: 9.8.2024</p>

        <p>
          <span class="font-bold">Introduction:</span> This Privacy Policy
          describes how CS2 Market Sniper ("we," "our," or "us") collects, uses,
          and discloses information when you use our bot ("Snipe Bot") on
          Discord. By using the Snipe Bot, you consent to the data practices
          described in this policy.
        </p>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">1. Information We Collect</h3>
          <p>
            <span class="font-bold">User Data:</span> We collect your Discord
            User ID and username when you interact with the bot.
          </p>
          <p>
            <span class="font-bold">Usage Data:</span> We may collect data on
            how you interact with the bot, such as commands issued and frequency
            of use.
          </p>
          <p>
            <span class="font-bold">Server Data:</span> We collect server IDs
            and channel information where the bot is used.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">2. How We Use Information</h3>
          <p>
            <span class="font-bold">Provide Services:</span> We use the data to
            operate, maintain, and improve the Snipe Bot’s functionality.
          </p>
          <p>
            <span class="font-bold">Communications:</span> We may use your
            information to communicate with you, including sending updates or
            support messages.
          </p>
          <p>
            <span class="font-bold">Data Analysis:</span> We may analyze usage
            data to enhance user experience and develop new features.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">3. Data Sharing</h3>
          <p>
            <span class="font-bold">Third-Party Services:</span> We do not share
            your data with third parties except for the services necessary to
            operate the bot (e.g., hosting services).
          </p>
          <p>
            <span class="font-bold">Legal Compliance:</span> We may disclose
            your information if required by law or to protect our rights.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">4. Data Security</h3>
          <p>
            We implement appropriate security measures to protect your data.
            However, no method of transmission over the internet is completely
            secure, and we cannot guarantee absolute security.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">5. Data Retention</h3>
          <p>
            We retain your data for as long as necessary to provide the Snipe
            Bot services or as required by law.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">6. Your Rights</h3>
          <p>
            You have the right to access, modify, or delete your personal data.
            You may also object to the processing of your data under certain
            circumstances.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">7. Changes to This Policy</h3>
          <p>
            We may update this Privacy Policy from time to time. We will notify
            users of any significant changes by posting the new policy on our
            website or through a notice in the bot.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">8. Contact Us</h3>
          <p>
            If you have any questions or concerns about this Privacy Policy,
            please contact us at:
            <a
              href="https://discord.com/invite/csbay-cs2-trading-642813124629757953"
              class="text-blue-500 underline"
              >https://discord.com/invite/csbay-cs2-trading-642813124629757953</a
            >
          </p>
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
