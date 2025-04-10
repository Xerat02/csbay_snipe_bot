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
        <h2 class="text-2xl font-extrabold">Terms of Service</h2>
        <p>Effective Date: 9.8.2024</p>

        <p>
          <span class="font-bold">Introduction:</span> These Terms of Service
          ("Terms") govern your use of CS2 Market Sniper ("we," "our," or "us")
          bot ("Snipe Bot") on Discord. By using the Snipe Bot, you agree to
          these Terms. If you do not agree, do not use the bot.
        </p>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">1. Use of the Bot</h3>
          <p>
            <span class="font-bold">Eligibility:</span> You must have a valid
            Discord account to use the Snipe Bot.
          </p>
          <p>
            <span class="font-bold">Compliance:</span> You agree to use the bot
            in compliance with all applicable laws and Discord's terms of
            service.
          </p>
          <p>
            <span class="font-bold">Prohibited Activities:</span> You may not
            use the bot to engage in activities that are harmful, illegal, or
            infringe on the rights of others.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">2. Termination</h3>
          <p>
            <span class="font-bold">Termination by Us:</span> We reserve the
            right to terminate or suspend your access to the Snipe Bot at our
            sole discretion, without notice or liability, for any reason.
          </p>
          <p>
            <span class="font-bold">Termination by You:</span> You may stop
            using the Snipe Bot at any time.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">3. Limitation of Liability</h3>
          <p>
            To the fullest extent permitted by law, we shall not be liable for
            any indirect, incidental, special, consequential, or punitive
            damages arising out of your use of or inability to use the Snipe
            Bot.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">4. Disclaimer of Warranties</h3>
          <p>
            The Snipe Bot is provided "as is" and "as available" without any
            warranties, express or implied, including but not limited to
            warranties of merchantability, fitness for a particular purpose, or
            non-infringement.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">5. Changes to the Terms</h3>
          <p>
            We may update these Terms from time to time. If we make significant
            changes, we will notify users by posting the new terms on our
            website or through a notice in the bot.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">6. Governing Law</h3>
          <p>
            These Terms are governed by and construed in accordance with the
            laws of Czech Republic, without regard to its conflict of law
            principles.
          </p>
        </div>

        <div class="space-y-6">
          <h3 class="text-xl font-extrabold">7. Contact Us</h3>
          <p>
            If you have any questions or concerns about these Terms of Service,
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
