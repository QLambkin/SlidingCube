using UnityEngine;

public class PlayerMovement : MonoBehaviour
{ 
    public Rigidbody rb;                //rigidbody variable

    public float forwardForce = 2000f;  //amount of force forward
    public float sidewaysForce = 500f;  //amount of force each side

    void FixedUpdate()
    {
        rb.AddForce(0, 0, sidewaysForce * Time.deltaTime, ForceMode.VelocityChange);        //adds force to rigidbody

        if (Input.GetKey("a"))
        {
            rb.AddForce(-sidewaysForce * Time.deltaTime, 0, 0, ForceMode.VelocityChange);   //adds force to the left when pressing a
        }

        if (Input.GetKey("d"))
        {
            rb.AddForce(sidewaysForce * Time.deltaTime, 0, 0, ForceMode.VelocityChange);    //adds force to the right when pressing d
        }

        if (rb.position.y < 0f)
        {
            FindObjectOfType<GameManager>().EndGame();  //end game if player falls off the map
        }
    }

}
