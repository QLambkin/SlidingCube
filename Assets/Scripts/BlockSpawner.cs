using UnityEngine;
using System.Collections.Generic;

public class BlockSpawner : MonoBehaviour
{
    public Transform[] spawnPoints;         //where the blocks spawn
    public GameObject blockPrefab;          //block prefab
    private float timeToSpawn = 0f;         //time until spawn
    private float timeBetweenWaves = 0.5f;  //time variable added between blocks spawning
    private Vector3 newPos;                 //next position for blocks to spawn
    private int x = 0;                      //increments distance of spawn position
    private int j = 0;                      //number of blocks spawned + 1
    private int k = 500;                    //check points which increment number of blocks spawned
    List<int> spawned = new List<int>();    //list of blocks spawned in a single row

    void Update()
    {
        //if its time to spawn blocks, call SpawnBlocks and increase the time to spawn by timeBetweenSpawn
        if(Time.time >= timeToSpawn)
        {
            SpawnBlocks();
            timeToSpawn = Time.time + timeBetweenWaves;
        }
    }

    void SpawnBlocks()
    {
        //get a random number to be the index of a spawn point until number of spawn points == number of blocks to be spawned
        //allows for fewer blocks to be spawned than ceiling number of blocks allowed to spawn
        for(int i = 0; i <= j; i++)
        {
            int randomIndex = Random.Range(0, spawnPoints.Length);

            //add index to list if index has not already been added in this row
            if (!spawned.Contains(randomIndex))
            {
                spawned.Add(randomIndex);

                newPos = spawnPoints[randomIndex].transform.position;   //selects spawn point position for block to be spawned
                newPos.z += x;                                          //increments spawn point down the map by x ammount
                Instantiate(blockPrefab, newPos, Quaternion.identity);  //spawns block at new location
            }
        }

        spawned.Clear();    //clears list of spawn point indeces

        x += 25;            //increment position down the map

        /*if x has hit a checkpoint and fewer than the total amount of spawn points -1 are spawning blocks,
        * then increment number of blocks spawning and double the checkpoint distance
        * stop at 1 less than total spawn points to allow the player a path to continue
        */
        if (x % k == 0 && j < spawnPoints.Length - 1)
        {
            j++;
            k *= 2;
        }
    }
}
