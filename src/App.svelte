<svelte:head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css">
</svelte:head>

<script>
  import { onMount } from "svelte";

  let username;
  let password;
  let isAuthenticated = false;
  let csrf = document.getElementsByName("csrf-token")[0].content;

  onMount(() => {
    fetch("/api/getsession", {
      credentials: "include",
    })
    .then((res) => res.json())
    .then((data) => {
      console.log(data);
      if (data.login == true) {
        isAuthenticated = true;
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
      }
    })
    .catch((err) => {
      console.log(err);
    });
  };

  const register = () => {
    fetch("/api/register", {
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
      if (data.register == false) {
        console.log("register failed");
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
    })
    .catch((err) => {
      console.log(err);
    });
  };
</script>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }

  .background {
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
  }

  .navbar {
    width: 100%;
    height: 100px;
  }

  .login {
    height: fit-content;
    width: fit-content;
    margin-top: auto;
    margin-bottom: auto;
  }
</style>


<div class="text-white bg-dark background">
  <div class="login" sm>
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
        <button type="button" on:click={register}>register</button>
      </form>
      <a href="/test">test</a>
    {/if}
  </div>
</div>