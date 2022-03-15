using UnityEngine;

public class PlayerCollision : MonoBehaviour
{ 
    public PlayerMovement movement;     //movement variable

    void OnCollisionEnter(Collision collisionInfo)
    {
        Debug.Log(collisionInfo.collider.name);
        
        //if player collides with an obstacle, disable players ability to move and end game
        if(collisionInfo.collider.tag == "Obstacle")
        {
            movement.enabled = false;
            FindObjectOfType<GameManager>().EndGame();
        }
    }
}
