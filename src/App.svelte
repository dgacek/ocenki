<script>
  import { onMount } from "svelte";

  let username;
  let password;
  let isAuthenticated = false;
  let csrf = document.getElementsByName("csrf-token")[0].content;
  let currentPage = "main" //main, profile
  let loginAlertContainer;

  onMount(() => {
    fetch("/api/getsession", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log(data);
        if (data.login == true) {
          isAuthenticated = true;
          username = data.username;
        } else {
          isAuthenticated = false;
        }
      })
      .catch((err) => {
        console.log(err);
      });
  });

  const createAlert = (type, message) => { //type == bootstrap color name
    return [
            `<div class="alert alert-${type} alert-dismissible" role="alert">`,
            `   <div>${message}</div>`,
            '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
            '</div>'
          ].join('')
  }

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
          password = "";
        } else {
          loginAlertContainer.innerHTML = createAlert("danger", "Login failed - incorrect credentials");
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
          loginAlertContainer.innerHTML = createAlert("danger", "Register failed - user already exists");
        } else {
          password = "";
        }
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

<svelte:head>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.1/dist/css/bootstrap.min.css"/>
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
</svelte:head>

<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }

  .login-background {
    height: 100%;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
  }

  .login {
    height: fit-content;
    width: fit-content;
    margin: auto;
    z-index: 1;
  }

  .login-alert-container {
    position: fixed;
    bottom: 10px;
    z-index: 999;
  }
</style>
  
{#if isAuthenticated}
  {#if currentPage === "main"}
    <h1>main page ({username})</h1>
    <button type="button" on:click={() => {currentPage = "profile"}}>profile</button>
    <button type="button" on:click={logout}>logout</button>
  {:else if currentPage === "profile"}
    <h1>user profile ({username})</h1>
    <button type="button" on:click={() => {currentPage = "main"}}>main page</button>
    <button type="button" on:click={logout}>logout</button>
  {/if}
{:else}
  <div class="login-background">
    <div class="login">
      <form id="form">
        <div class="row mb-3">
          <h1 class="display-6">Log in</h1>
        </div>
        <div class="row mb-3">
          <input type="text" class="form-control" placeholder="Username" bind:value={username} />
        </div>
        <div class="row mb-3">
          <input type="password" class="form-control" placeholder="Password" bind:value={password} />
        </div>
        <div class="row justify-content-evenly">
          <button type="button" class="btn btn-primary col-5" on:click={login}>Login</button>
          <button type="button" class="btn btn-secondary col-5" on:click={register}>Register</button>
        </div>
      </form>
    </div>
    <div class="login-alert-container" bind:this={loginAlertContainer}></div>
  </div>
  
{/if}
  