<!--Header section-->
<!--mobile navbar-->
<nav
  class="z-[200] sticky top-0 hidden flex-col justify-center items-center backdrop-blur-lg !w-screen !h-screen text-[22px]"
  id="mobile_menu"
>
  <img
    src="media/cross.png"
    alt="Menu close icon"
    class="absolute top-3 right-3 w-[40px]"
    onclick="mobile_nav()"
  />
  <a href="index.php">Home</a>
  <a href="snipes.php">Online</a>
  <a href="servers.php">Servers</a>
  <a href="setup.php">Setup</a>
  <a href="index.php#faq">FAQ</a>
</nav>
<div class="w-[90%] lg:max-w-[1240px] mx-auto pt-10 space-y-24 py-24">
<header
      class="shadow-[0_20px_50px_rgba(106,_160,_238,_0.2)] backdrop-blur-lg z-10 lg:sticky lg:top-12 flex flex-row items-center justify-center lg:justify-between text-[18px] border-2 border-[#272c31] py-5 px-2 lg:px-5 rounded-2xl bg-[#181b1ed0]"
    >
      <a class="flex flex-row w-full lg:w-max" href="index.php">
        <img
        src="media/csbay_logo_icon.jpg"
        alt="CSBAY logo icon"
        class="mr-2 w-[50px] rounded-2xl"
        />
        <img
        src="media/csbay_logo.png"
        alt="CSBAY logo"
        />
      </a>
      <nav class="lg:flex flex-row hidden">
        <a class="mr-5" href="index.php">Home</a>
        <a class="mr-5" href="snipes.php">Online</a>
        <a class="mr-5" href="servers.php">Servers</a>
        <a class="mr-5" href="setup.php">Setup</a>
        <a class="mr-5" href="index.php#faq">FAQ</a>
      </nav>
      <a
          href="https://discord.com/oauth2/authorize?client_id=1104871916940050542&scope=bot&permissions=277025507328"
          target="_blank"
          class="hidden lg:flex justify-center items-center w-full lg:w-max px-6 py-2 bg-gradient-to-tr from-[#2655FD] to-[#4D62FB] rounded-2xl font-bold hover:scale-105 transition-all active::animate-ping"
        >
        <span class="mr-5 text-[12px] lg:text-[18px]">Add to Discord</span>
        <img
          src="media/discord_icon.png"
          alt="Discord icon"
          class="h-[40px] w-[40px]"
        />
      </a>
      <img
        src="media/menu-bar.png"
        alt="Menu bar logo"
        class="lg:hidden w-[40px] cursor-pointer"
        onclick="mobile_nav()"
      />
</header>