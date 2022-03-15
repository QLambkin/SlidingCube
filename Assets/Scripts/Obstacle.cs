using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Obstacle : MonoBehaviour
{
    private Transform player;   //player variable

    private void Start()
    {
        //grabs player from game manager
        player = FindObjectOfType<GameManager>().player;
    }

    void Update()
    {
        if(transform.position.z < player.position.z - 20)
        {
            //destroys obstacles after the player passes them
            Destroy(gameObject);
        }
    }
}
