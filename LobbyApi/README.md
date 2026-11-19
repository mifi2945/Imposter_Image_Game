Lobby Object: 
name: string
code: string
userIds: number[]
round: number

GET /lobbies
Get a list of all lobbies
200 - Returns a list of Lobby objects
401 - Unauthorized (user not logged in)
GET /lobbies/{id}
Get a lobby by id
200 - Returns a Lobby object
401 - Unauthorized (user not logged in)
404 - Not Found
POST /lobbies/new
Create a new lobby
Body: NewLobbyRequestBody
creatorUserId: number
lobbyName: string
201 - Success, returns created lobby object
400 - Validation failed
401 - Unauthorized (user not logged in)
POST /lobbies/start
Start game
 POST /game/startGame
POST /lobbies/join/ws
username: string
game_id?: number

DELETE /game/removePlayer/{game_id}/{username}

POST /votes
suspect_username: string
username: string
send vote status to other players thru lobby connection
POST /votes