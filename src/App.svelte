<script>
  import { onMount } from "svelte";
  import { JSONPath } from '../node_modules/jsonpath-plus/dist/index-browser-esm.js';


  let username;
  let password;
  let isAuthenticated = false;
  let csrf = document.getElementsByName("csrf-token")[0].content;
  let currentPage = "main" //main, profile
  let loginAlertContainer;
  let searchQuery;
  let items = [];
  let myratings = [];
  let rangeValue = 50;
  

  onMount(() => {
    fetch("/api/getsession", {
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
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


  const login = (event) => {
    event.preventDefault();
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
        items = [];
        searchQuery = "";
      })
      .catch((err) => {
        console.log(err);
      });
  };


  const search = (event) => {
    event.preventDefault();
    fetch(`/api/search?q=${searchQuery.replace('&', '%26')}`, {
      method: "GET",
      credentials: "include",
      headers: {
        "X-CSRFToken": csrf
      }
    })
      .then((res) => res.json())
      .then((data) => {
        items = data.albums.items;
      })
      .catch((err) => {
        console.log(err);
      });
  };


  const rate = (album_id, array_index) => {
    fetch("/api/rate", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
      },
      credentials: "include",
      body: JSON.stringify({ album_id: album_id, rating: rangeValue }),
    })
      .then((res) => res.json())
      .then((data) => {
        window.bootstrap.Collapse.getInstance(document.getElementById(`collapse${album_id}`)).hide();
        items[array_index].average_rating = data.average_rating;
        items[array_index].ratings_count = data.ratings_count;
        items[array_index].current_user_rating = data.current_user_rating;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const rate_update = (album_id, array_index) => {
    fetch("/api/rate", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
      },
      credentials: "include",
      body: JSON.stringify({ album_id: album_id, rating: rangeValue }),
    })
      .then((res) => res.json())
      .then((data) => {
        window.bootstrap.Collapse.getInstance(document.getElementById(`collapse${album_id}`)).hide();
        items[array_index].average_rating = data.average_rating;
        items[array_index].ratings_count = data.ratings_count;
        items[array_index].current_user_rating = data.current_user_rating;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const rate_update_2 = (album_id, array_index) => {
    fetch("/api/rate", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
      },
      credentials: "include",
      body: JSON.stringify({ album_id: album_id, rating: rangeValue }),
    })
      .then((res) => res.json())
      .then((data) => {
        window.bootstrap.Collapse.getInstance(document.getElementById(`collapse${album_id}`)).hide();
        myratings[array_index].average_rating = data.average_rating;
        myratings[array_index].ratings_count = data.ratings_count;
        myratings[array_index].current_user_rating = data.current_user_rating;
        items = [];
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const rate_delete = (album_id, array_index) => {
    fetch("/api/rate", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
      },
      credentials: "include",
      body: JSON.stringify({ album_id: album_id }),
    })
      .then((res) => res.json())
      .then((data) => {
        window.bootstrap.Collapse.getInstance(document.getElementById(`collapse${album_id}`)).hide();
        items[array_index].average_rating = data.average_rating;
        items[array_index].ratings_count = data.ratings_count;
        items[array_index].current_user_rating = data.current_user_rating;
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const rate_delete_2 = (album_id, array_index) => {
    fetch("/api/rate", {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrf,
      },
      credentials: "include",
      body: JSON.stringify({ album_id: album_id }),
    })
      .then((res) => res.json())
      .then((data) => {
        let myratings2 = myratings;
        myratings2.splice(array_index, 1);
        myratings = myratings2;
        items = [];
      })
      .catch((err) => {
        console.log(err);
      });
  };

  const get_my_ratings = () => {
    fetch(`/api/myratings`, {
      method: "GET",
      credentials: "include",
      headers: {
        "X-CSRFToken": csrf
      }
    })
      .then((res) => res.json())
      .then((data) => {
        myratings = data.albums;
      })
      .catch((err) => {
        console.log(err);
      });
  };

</script>


<svelte:head>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
  <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-kenU1KFdBIe4zVF0s0G1M5b4hcpxyD9F7jL+jjXkk+Q2h455rYXK/7HAuoJl+0I4" crossorigin="anonymous"></script>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@48,100,1,0" />
</svelte:head>


<style>
  :global(body) {
    margin: 0;
    padding: 0;
  }

  :global(a[class*="nav-link"]:visited) {
    color: var(--bs-nav-link-color);
  }

  :global(a[class*="badge"]:visited) {
    color: var(--bs-badge-color);
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

  .text-outline {
    text-shadow: -1px -1px 0 #000, 1px -1px 0 #000, -1px 1px 0 #000, 1px 1px 0 #000;
  }
</style>
  

{#if isAuthenticated}
  <header class="navbar navbar-expand-lg bg-dark navbar-dark">
    <div class="container-fluid">
      <span class="navbar-brand">Ocenki for Spotify</span>
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
          <li class="nav-item">
            {#if currentPage === "main"}
              <!-- svelte-ignore a11y-invalid-attribute -->
              <a class="nav-link active" href="#">Home</a>
            {:else}
              <!-- svelte-ignore a11y-invalid-attribute -->
              <a class="nav-link" on:click={() => {currentPage = "main"}} href="#">Home</a>
            {/if}
          </li>
          <li class="nav-item">
            {#if currentPage === "profile"}
              <!-- svelte-ignore a11y-invalid-attribute -->
              <a class="nav-link active" href="#">My ratings</a>
            {:else}
              <!-- svelte-ignore a11y-invalid-attribute -->
              <a class="nav-link" on:click={() => {get_my_ratings(); currentPage = "profile";}} href="#">My ratings</a>
            {/if}
          </li>
        </ul>
        <div class="dropdown">
          <button class="btn btn-dark material-symbols-outlined dropdown-toggle" data-bs-toggle="dropdown" data-bs-display="static">
            account_circle
          </button>
          <ul class="dropdown-menu dropdown-menu-lg-end">
            <div class="ps-3"><small>Logged in as</small><br>{username}</div>
            <li><hr class="dropdown-divider"></li>
            <!-- svelte-ignore a11y-invalid-attribute -->
            <li><a class="dropdown-item text-danger" href="#" on:click={logout}>Logout</a></li>
          </ul>
        </div>
      </div>
    </div>
  </header>

  {#if currentPage === "main"}
    <div class="container-sm mt-3">
      <div class="row justify-content-center">
        <form on:submit={search}>
          <div class="input-group">
            <input class="form-control form-control-lg" type="text" bind:value={searchQuery} placeholder="Search">
            <button class="btn btn-outline-secondary" type="button" on:click={search}>
              <span class="material-symbols-outlined pt-2">
                search
              </span>
            </button>
          </div>
        </form>
      </div>
      <ul class="list-group">
        {#each items as element}
        <li class="list-group-item">
          <div class="row">
            <div class="col-auto">
              <img src="{element.images[1].url}" class="img-thumbnail" width="200" height="200" alt="thumbnail">
            </div>
            <div class="col">
              <div class="row">
                <div class="col">
                  <small class="text-muted">{element.album_type}</small><br>
                  <p><span class="h3">{element.name} </span><a class="badge rounded-pill bg-success btn" href="{element.external_urls.spotify}" target="_blank" rel="noopener noreferrer">Play on Spotify</a></p>
                  <p class="text-muted">{JSONPath({path: "$.artists[*].name", json: element}).join(', ')}</p>
                  <small class="text-muted">{element.release_date.split("-")[0]}</small>
                </div>
                <div class="col text-end">
                  {#if element.average_rating === -1}
                    <p class="text-muted">No ratings</p>
                  {:else}
                    <figure class="figure img-thumbnail text-white {element.average_rating < 40 ? "bg-danger" : (element.average_rating < 70 ? "bg-warning" : "bg-success")}">
                      <p class="display-4 fw-semibold text-outline">{element.average_rating === 100 ? element.average_rating/10 : (element.average_rating/10).toFixed(1)}</p>
                    </figure><br>
                    <small class="text-muted">Average from {element.ratings_count} rating{element.ratings_count === 1 ? '' : 's'}</small>
                  {/if}
                  {#if element.current_user_rating === -1}
                    <p class="text-muted">Not yet rated by you</p>
                    <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{element.id}" aria-expanded="false" aria-controls="collapse{element.id}">Rate</button>
                  {:else}
                    <p class="text-muted">Your rating: {element.current_user_rating === 100 ? element.current_user_rating/10 : (element.current_user_rating/10).toFixed(1)}</p>
                    <button class="btn btn-outline-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{element.id}" aria-expanded="false" aria-controls="collapse{element.id}" on:click={() => rangeValue = element.current_user_rating}>Change rating</button>
                  {/if}
                </div>
              </div>
              <div class="collapse mt-3" id="collapse{element.id}">
                <div class="card card-body">
                  <div class="row align-items-center justify-content-evenly">
                    <div class="col-2 d-flex align-items-center justify-content-center" style="width: 12.5%">
                      <figure class="figure img-thumbnail text-white my-auto {rangeValue < 40 ? "bg-danger" : (rangeValue < 70 ? "bg-warning" : "bg-success")}">
                        <p class="display-4 fw-semibold text-outline">{rangeValue === 100 ? rangeValue/10 : (rangeValue/10).toFixed(1)}</p>
                      </figure>
                    </div>
                    <div class="col d-flex justify-content-center">
                      <input type="range" class="form-range" id="range{element.id}" min="0" max="100" step="5" bind:value={rangeValue}>
                    </div>
                    <div class="col-2 d-flex flex-column justify-content-center">
                      {#if element.current_user_rating === -1}
                        <button class="btn btn-primary" type="button" on:click={() => {rate(element.id, items.indexOf(element))}}>Rate</button>
                      {:else}
                        <button class="btn btn-primary m-1" type="button" on:click={() => {rate_update(element.id, items.indexOf(element))}}>Change rating</button>
                        <button class="btn btn-danger m-1" type="button" on:click={() => {rate_delete(element.id, items.indexOf(element))}}>Delete rating</button>
                      {/if}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </li>
        {/each}
      </ul>
    </div>
  {:else if currentPage === "profile"}
    <div class="container-sm mt-3">
      <ul class="list-group">
        {#each myratings as element}
        <li class="list-group-item">
          <div class="row">
            <div class="col-auto">
              <img src="{element.images[1].url}" class="img-thumbnail" width="200" height="200" alt="thumbnail">
            </div>
            <div class="col">
              <div class="row">
                <div class="col">
                  <small class="text-muted">{element.album_type}</small><br>
                  <p><span class="h3">{element.name} </span><a class="badge rounded-pill bg-success btn" href="{element.external_urls.spotify}" target="_blank" rel="noopener noreferrer">Play on Spotify</a></p>
                  <p class="text-muted">{JSONPath({path: "$.artists[*].name", json: element}).join(', ')}</p>
                  <small class="text-muted">{element.release_date.split("-")[0]}</small>
                </div>
                <div class="col text-end">
                  {#if element.average_rating === -1}
                    <p class="text-muted">No ratings</p>
                  {:else}
                    <figure class="figure img-thumbnail text-white {element.average_rating < 40 ? "bg-danger" : (element.average_rating < 70 ? "bg-warning" : "bg-success")}">
                      <p class="display-4 fw-semibold text-outline">{element.average_rating === 100 ? element.average_rating/10 : (element.average_rating/10).toFixed(1)}</p>
                    </figure><br>
                    <small class="text-muted">Average from {element.ratings_count} rating{element.ratings_count === 1 ? '' : 's'}</small>
                  {/if}
                  {#if element.current_user_rating === -1}
                    <p class="text-muted">Not yet rated by you</p>
                    <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{element.id}" aria-expanded="false" aria-controls="collapse{element.id}">Rate</button>
                  {:else}
                    <p class="text-muted">Your rating: {element.current_user_rating === 100 ? element.current_user_rating/10 : (element.current_user_rating/10).toFixed(1)}</p>
                    <button class="btn btn-outline-primary" type="button" data-bs-toggle="collapse" data-bs-target="#collapse{element.id}" aria-expanded="false" aria-controls="collapse{element.id}" on:click={() => rangeValue = element.current_user_rating}>Change rating</button>
                  {/if}
                </div>
              </div>
              <div class="collapse mt-3" id="collapse{element.id}">
                <div class="card card-body">
                  <div class="row align-items-center justify-content-evenly">
                    <div class="col-2 d-flex align-items-center justify-content-center" style="width: 12.5%">
                      <figure class="figure img-thumbnail text-white my-auto {rangeValue < 40 ? "bg-danger" : (rangeValue < 70 ? "bg-warning" : "bg-success")}">
                        <p class="display-4 fw-semibold text-outline">{rangeValue === 100 ? rangeValue/10 : (rangeValue/10).toFixed(1)}</p>
                      </figure>
                    </div>
                    <div class="col d-flex justify-content-center">
                      <input type="range" class="form-range" id="range{element.id}" min="0" max="100" step="5" bind:value={rangeValue}>
                    </div>
                    <div class="col-2 d-flex flex-column justify-content-center">
                      {#if element.current_user_rating === -1}
                        <button class="btn btn-primary" type="button" on:click={() => {rate(element.id, myratings.indexOf(element))}}>Rate</button>
                      {:else}
                        <button class="btn btn-primary m-1" type="button" on:click={() => {rate_update_2(element.id, myratings.indexOf(element))}}>Change rating</button>
                        <button class="btn btn-danger m-1" type="button" on:click={() => {rate_delete_2(element.id, myratings.indexOf(element))}}>Delete rating</button>
                      {/if}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </li>
        {/each}
      </ul>
    </div>
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
          <button type="submit" class="btn btn-primary col-5" on:click={login}>Login</button>
          <button type="button" class="btn btn-secondary col-5" on:click={register}>Register</button>
        </div>
      </form>
    </div>
    <div class="login-alert-container" bind:this={loginAlertContainer}></div>
  </div>
  
{/if}
  