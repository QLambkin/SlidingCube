using UnityEngine;
using UnityEngine.UI;
using System.Collections;
using UnityEngine.SceneManagement;

public class GameManager : MonoBehaviour
{
    bool gameHasEnded = false;      //whether player is alive and game is running
    float slowTime = 10f;           //how slow slowmo time will be (higher = slower)

    public Transform player;        //player variable
    public Text scoreText;          //text for the running score
    public Text highScoreText;      //text for the high score
    public GameObject deathUI;      //transition UI for when the player dies

    void Start()
    {
        //grabs the high score
        highScoreText.text = PlayerPrefs.GetInt("Highscore", 0).ToString();
    }

    void FixedUpdate()
    {
        if (gameHasEnded == false)
        {
            if(player.position.z > PlayerPrefs.GetInt("Highscore", 0))
            {
                //update high score if the game is still running and the player has beaten the previous high score
                PlayerPrefs.SetInt("Highscore", (int)player.position.z);
            }

            PlayerPrefs.SetInt("Score", (int)player.position.z);                                //updates players current score
            scoreText.text = PlayerPrefs.GetInt("Score", (int)player.position.z).ToString();    //updates players current score text
            highScoreText.text = PlayerPrefs.GetInt("Highscore", 0).ToString();                 //updates players current high score text
        }
    }

    public void EndGame ()
    {
        if(gameHasEnded == false)       
        {
            gameHasEnded = true;        //gameHasEnded gets set to true
            Debug.Log("GAME OVER");     //Debug.Log prints "GAME OVER"
            deathUI.SetActive(true);    //death UI starts to fade
            StartCoroutine(SlowMo());   //SlowMo coroutine begins
        }
    }

    IEnumerator SlowMo()
    {

        Time.timeScale = 1f / slowTime;                         //sets timeScale
        Time.fixedDeltaTime = Time.fixedDeltaTime / slowTime;   //sets time

        yield return new WaitForSeconds(1.6f / slowTime);       //waits set amount of time for slowmo
        SceneManager.LoadScene("Credits");                      //loads credits

        Time.timeScale = 1f;                                    //resets timescale
        Time.fixedDeltaTime = Time.fixedDeltaTime * slowTime;   //resets time
    }

    void Credits()
    {
        SceneManager.LoadScene("Credits");      //loads the credits scene
    }
}
