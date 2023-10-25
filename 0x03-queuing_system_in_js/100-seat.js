import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';


const app = express();
const port = 1245;
const redisClient = redis.createClient();
const getAsync = promisify(redisClient.get).bind(redisClient);
const key = 'available_seats';
const queue = kue.createQueue();
const reservationsQueue = 'reserve_seat';
let reservationEnabled;

function reserveSeat(number) {
  redisClient.set(key, number);
}

async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync(key);
  return availableSeats;
}

redisClient.on('connect', () => {
  console.log('Redis client connected to the server');

  reserveSeat(50);
  reservationEnabled = true;
});

redisClient.on('error', (error) => {
  console.log(`Redis client not connected to the server: ${error.message}`);
});

app.listen(port, () => {
  console.log(`app listening at http://localhost:${port}`);
});

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (reservationEnabled === false) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const jobData = {};

  const job = queue.create(reservationsQueue, jobData).save((err) => {
    if (err) {
      res.json({ status: 'Reservation failed' });
    } else {
      res.json({ status: 'Reservation in process' });
    }
  });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });

  job.on('failed', (errorMessage) => {
    console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
  });
});

app.get('/process', async (req, res) => {
  // Process the queue reserve_seat
  res.json({ status: 'Queue processing' });
});
