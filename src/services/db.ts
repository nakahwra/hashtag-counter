import { MongoClient } from 'mongodb';

export async function getConnection() {
  const uri = "mongodb://localhost:27017/";
  const client = new MongoClient(uri);

  await client.connect();
  return client;
}