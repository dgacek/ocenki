<script>
  import { onMount} from "svelte";
  import { io } from "socket.io-client";

  let username;
  let password;
  let isAuthenticated = false;
  let csrf = document.getElementsByName("csrf-token")[0].content;
  var socket;

  onMount(() => {
    fetch("/api/getsession", {
      credentials: "include",
    })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if (data.login == true) {
        isAuthenticated = true;
        socket = io();
      } else {
        isAuthenticated = false;
      }
    })
    .catch((err) => {
      console.log(err);
    });
  });

  const login = () => {
    fetch("/api/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
      },
      credentials: "include",
      body: JSON.stringify({ username: username, password: password }),
    })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if (data.login == true) {
        isAuthenticated = true;
        socket = io();
      }
    })
    .catch((err) => {
      console.log(err);
    });
  };

  const whoami = () => {
    fetch("/api/data", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
      },
      credentials: "include",
    })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      alert(`Welcome, ${data.username}!`);
    })
    .catch((err) => {
      console.log(err);
    });
  };

  const logout = () => {
    fetch("/api/logout", {
      credentials: "include",
    })
    .then(() => {
      isAuthenticated = false;
      socket.disconnect();
    })
    .catch((err) => {
      console.log(err);
    });
  };
</script>

<style>
  .container {
    padding-top: 10%;
  }
</style>

<center>
  <div class="container">
    {#if isAuthenticated}
      <h1>You are authenticated!</h1>
      <button type="button" on:click={whoami}>whoami</button>
      <button type="button" on:click={logout}>logout</button>
    {:else}
      <h1>Log in</h1>
      <form id="form">
        username:
        <input type="text" bind:value={username} />
        <br /><br />
        password:
        <input type="password" bind:value={password} /><br /><br />
        <button type="button" on:click={login}>login</button>
      </form>
    {/if}
  </div>
</center>
